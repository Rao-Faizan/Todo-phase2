"""Intent Detection Service for identifying task-related intents in user messages"""

from enum import Enum
from typing import NamedTuple
from pydantic import BaseModel


class TaskIntent(Enum):
    ADD_TASK = "add_task"
    LIST_TASKS = "list_tasks"
    COMPLETE_TASK = "complete_task"
    UPDATE_TASK = "update_task"
    DELETE_TASK = "delete_task"
    GENERAL_CONVERSATION = "general_conversation"


class IntentResult(NamedTuple):
    intent: TaskIntent
    confidence: float = 1.0
    entities: dict = None


class IntentDetectionService:
    def __init__(self):
        self.intents_keywords = {
            TaskIntent.ADD_TASK: [
                "add", "create", "make", "new", "put", "include", "want to",
                "need to", "have to", "should", "must", "plan to", "going to"
            ],
            TaskIntent.LIST_TASKS: [
                "show", "list", "display", "view", "see", "all", "my",
                "what", "do i have", "check", "browse"
            ],
            TaskIntent.COMPLETE_TASK: [
                "complete", "done", "finish", "mark done", "accomplish",
                "finished", "tick off", "cross off", "remove"
            ],
            TaskIntent.UPDATE_TASK: [
                "update", "change", "modify", "edit", "adjust", "revise",
                "improve", "fix", "alter"
            ],
            TaskIntent.DELETE_TASK: [
                "delete", "remove", "erase", "cancel", "get rid of",
                "eliminate", "trash", "dispose", "drop"
            ]
        }

    async def detect_intent(self, message: str) -> IntentResult:
        """
        Detect the intent from the user message
        """
        message_lower = message.lower().strip()

        # Check for keywords for each intent
        scores = {}
        for intent, keywords in self.intents_keywords.items():
            score = sum(1 for keyword in keywords if keyword in message_lower)
            scores[intent] = score

        # Find the intent with the highest score
        best_intent = max(scores, key=scores.get)
        best_score = scores[best_intent]

        # If no keywords match, default to general conversation
        if best_score == 0:
            return IntentResult(intent=TaskIntent.GENERAL_CONVERSATION, confidence=0.5)

        # Calculate confidence based on the score
        total_keywords = sum(len(keywords) for keywords in self.intents_keywords.values())
        confidence = min(best_score / max(len(self.intents_keywords[best_intent]), 1), 1.0)

        return IntentResult(intent=best_intent, confidence=min(confidence, 1.0))


# Global instance
intent_detection_service = IntentDetectionService()