"""Error Handler for MCP Server"""

import logging
from typing import Dict, Any, Optional
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import traceback


# Set up logger
logger = logging.getLogger(__name__)


class MCPServerError(Exception):
    """Base exception class for MCP server errors"""
    def __init__(self, message: str, error_code: str = "INTERNAL_ERROR", status_code: int = 500):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.status_code = status_code


class ValidationError(MCPServerError):
    """Exception raised for validation errors"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "VALIDATION_ERROR", 400)
        self.details = details or {}


class AuthenticationError(MCPServerError):
    """Exception raised for authentication errors"""
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, "AUTHENTICATION_ERROR", 401)


class AuthorizationError(MCPServerError):
    """Exception raised for authorization errors"""
    def __init__(self, message: str = "Not authorized"):
        super().__init__(message, "AUTHORIZATION_ERROR", 403)


class ResourceNotFoundError(MCPServerError):
    """Exception raised when a resource is not found"""
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, "RESOURCE_NOT_FOUND", 404)


class RateLimitExceededError(MCPServerError):
    """Exception raised when rate limit is exceeded"""
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(message, "RATE_LIMIT_EXCEEDED", 429)


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Global exception handler for the MCP server"""
    # Log the full exception with traceback
    logger.error(f"Unhandled exception occurred: {exc}", exc_info=True)

    # Create a generic error response
    error_response = {
        "success": False,
        "error": "An unexpected error occurred",
        "error_code": "INTERNAL_ERROR",
        "details": None
    }

    # Return a 500 error response
    return JSONResponse(
        status_code=500,
        content=error_response
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    """Handler for HTTP exceptions"""
    logger.warning(f"HTTP exception: {exc.status_code} - {exc.detail}")

    error_response = {
        "success": False,
        "error": exc.detail if isinstance(exc.detail, str) else str(exc.detail),
        "error_code": f"HTTP_{exc.status_code}",
        "status_code": exc.status_code,
        "details": None
    }

    return JSONResponse(
        status_code=exc.status_code,
        content=error_response
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handler for request validation errors"""
    logger.warning(f"Validation error: {exc.errors()}")

    # Format validation errors
    error_details = []
    for error in exc.errors():
        error_details.append({
            "location": " -> ".join(str(loc) for loc in error['loc']),
            "message": error['msg'],
            "type": error['type']
        })

    error_response = {
        "success": False,
        "error": "Validation failed",
        "error_code": "VALIDATION_ERROR",
        "status_code": 400,
        "details": error_details
    }

    return JSONResponse(
        status_code=400,
        content=error_response
    )


def setup_error_handlers(app):
    """Setup error handlers for the FastAPI app"""
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, global_exception_handler)

    return app