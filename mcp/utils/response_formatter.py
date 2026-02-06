"""Tool Response Formatter for MCP Server"""

from typing import Any, Dict, Optional
from pydantic import BaseModel
import json


class ToolResponseFormat(BaseModel):
    """Standard format for tool responses"""
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    action: str


class ToolResponseFormatter:
    """Utility class for formatting tool responses consistently"""

    @staticmethod
    def format_success(data: Any, action: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Format a successful tool response"""
        return ToolResponseFormat(
            success=True,
            data=data,
            error=None,
            metadata=metadata or {},
            action=action
        ).model_dump()

    @staticmethod
    def format_error(error_msg: str, action: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Format an error tool response"""
        return ToolResponseFormat(
            success=False,
            data=None,
            error=error_msg,
            metadata=metadata or {},
            action=action
        ).model_dump()

    @staticmethod
    def format_validation_error(errors: list, action: str) -> Dict[str, Any]:
        """Format a validation error response"""
        return ToolResponseFormat(
            success=False,
            data=None,
            error=f"Validation failed: {', '.join(errors)}",
            metadata={"validation_errors": errors},
            action=action
        ).model_dump()


# Global instance
tool_response_formatter = ToolResponseFormatter()