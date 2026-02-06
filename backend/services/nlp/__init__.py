"""NLP Services for Natural Language Processing"""

from .intent_detection_service import intent_detection_service, TaskIntent
from .task_extraction_service import task_extraction_service

__all__ = [
    "intent_detection_service",
    "TaskIntent",
    "task_extraction_service"
]