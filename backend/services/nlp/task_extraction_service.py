"""Task Extraction Service for extracting task details from user messages"""

from pydantic import BaseModel
from typing import Optional
import re
from datetime import datetime


class ExtractedTask(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[str] = None
    priority: Optional[str] = None


class TaskExtractionService:
    def __init__(self):
        # Priority keywords
        self.priority_keywords = {
            'high': ['urgent', 'important', 'asap', 'soon', 'critical', 'high priority'],
            'low': ['later', 'whenever', 'eventually', 'when possible', 'low priority'],
            'medium': []  # Default priority
        }

    async def extract_task_details(self, message: str, agent_service=None) -> ExtractedTask:
        """
        Extract task details from a user message.
        If agent_service is provided, it uses the AI model for smarter extraction.
        """
        if agent_service and agent_service.openai_client:
            try:
                # Use AI for extraction
                prompt = f"""
                Extract task details from this message: "{message}"
                Return JSON with: title, description, due_date (YYYY-MM-DD), priority (high/medium/low).
                If a field is missing, use null.
                """
                
                response = await agent_service.openai_client.chat.completions.create(
                    model=agent_service.model_name,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=200
                )
                
                content = response.choices[0].message.content
                import json
                # Handle potential markdown code blocks
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0].strip()
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0].strip()
                    
                data = json.loads(content)
                return ExtractedTask(
                    title=data.get("title"),
                    description=data.get("description"),
                    due_date=data.get("due_date"),
                    priority=data.get("priority")
                )
            except Exception as e:
                print(f"AI Extraction failed: {e}, falling back to regex.")
        
        # Fallback to regex extraction
        # Extract priority first
        priority = self._extract_priority(message)

        # Extract due date
        due_date = self._extract_due_date(message)

        # Clean message for title
        cleaned_message = self._clean_message_for_task_extraction(message)
        
        # Remove priority markers from the cleaned message to avoid redundant titles
        for keywords in self.priority_keywords.values():
            for kw in keywords:
                cleaned_message = re.sub(rf'\b{kw}\b', '', cleaned_message, flags=re.IGNORECASE)
        
        # Remove task/to/for/etc again after priority removal
        cleaned_message = re.sub(r'\b(task|to|for|on|by)\b', '', cleaned_message, flags=re.IGNORECASE)
        
        # Determine title and description
        title, description = self._extract_title_and_description(cleaned_message)

        return ExtractedTask(
            title=title,
            description=description,
            due_date=due_date,
            priority=priority
        )

    def _clean_message_for_task_extraction(self, message: str) -> str:
        """Remove intent-indicating words to get to the core task content"""
        # Common phrases that indicate task creation but aren't part of the task itself
        intent_phrases = [
            r'\b(add|create|make|new|put|include|want to|need to|have to|should|must|plan to|going to)\s+',
            r'\b(to|for|on|by)\s+',  # Prepositions that might be part of intent
            r'^\s*please\s+',  # Politeness phrases
            r'^\s*i\s+(want|need|should|must|would like to)\s+',  # Common starting phrases
        ]

        cleaned = message.lower().strip()
        for pattern in intent_phrases:
            cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)

        return cleaned.strip()

    def _extract_due_date(self, message: str) -> Optional[str]:
        """Extract due date from message using regex patterns"""
        # Patterns for dates
        date_patterns = [
            r'tomorrow',
            r'next week',
            r'next \w+',
            r'next month',
            r'by (\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4})',  # MM/DD/YYYY or DD/MM/YYYY
            r'on (\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4})',  # MM/DD/YYYY or DD/MM/YYYY
            r'(\d{4}-\d{2}-\d{2})',  # YYYY-MM-DD
            r'in (\d+)\s*(day|days|week|weeks|month|months)',  # in X days/weeks/months
        ]

        for pattern in date_patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                if 'tomorrow' in match.group(0).lower():
                    tomorrow = datetime.now().date().replace(day=datetime.now().date().day + 1)
                    return str(tomorrow)
                elif 'next week' in match.group(0).lower():
                    # Return a placeholder for next week
                    return 'next week'
                elif 'next' in match.group(0).lower():
                    # Handle "next friday", "next monday", etc.
                    weekday_map = {'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6}
                    for day_name, day_num in weekday_map.items():
                        if day_name in match.group(0).lower():
                            today = datetime.now()
                            days_ahead = day_num - today.weekday()
                            if days_ahead <= 0: # Target day already happened this week
                                days_ahead += 7
                            days_ahead += 7 # "Next" often means the following week
                            target_date = today.replace(day=today.day + days_ahead)
                            return str(target_date.date())
                    return match.group(0)
                elif 'next month' in match.group(0).lower():
                    return 'next month'
                elif match.groups():  # Has captured groups (dates)
                    return match.group(1) if match.lastindex >= 1 else match.group(0)
                else:
                    return match.group(0)

        return None

    def _extract_priority(self, message: str) -> Optional[str]:
        """Extract priority from message based on keywords"""
        message_lower = message.lower()

        for priority, keywords in self.priority_keywords.items():
            for keyword in keywords:
                if keyword in message_lower:
                    return priority

        return None  # Default to medium priority

    def _extract_title_and_description(self, message: str) -> tuple[Optional[str], Optional[str]]:
        """Extract title and description from the cleaned message"""
        # For now, treat the entire cleaned message as the title
        # In a more advanced implementation, we could parse out sub-details
        if not message.strip():
            return None, None

        # Split on common separators to determine title vs description
        parts = re.split(r'[.:;,-]\s+', message, maxsplit=1)

        title = parts[0].strip().capitalize() if parts else None
        description = parts[1].strip() if len(parts) > 1 else None

        # If title is too short or doesn't make sense, use the whole message
        if not title or len(title.split()) < 2:
            title = message.strip().capitalize()

        return title, description


# Global instance
task_extraction_service = TaskExtractionService()