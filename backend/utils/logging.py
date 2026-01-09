import logging
from datetime import datetime
from typing import Any, Dict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the specified name"""
    return logging.getLogger(name)

def log_request(user_id: str, endpoint: str, method: str, ip_address: str = None) -> None:
    """Log API requests"""
    logger = get_logger("api_requests")
    logger.info(f"User {user_id} accessed {method} {endpoint} from {ip_address or 'unknown'}")

def log_authentication(user_id: str, success: bool, reason: str = None) -> None:
    """Log authentication events"""
    logger = get_logger("authentication")
    status = "SUCCESS" if success else "FAILED"
    message = f"Authentication {status} for user {user_id}"
    if reason:
        message += f" - Reason: {reason}"
    logger.info(message)

def log_security_event(event_type: str, user_id: str = None, details: Dict[str, Any] = None) -> None:
    """Log security-related events"""
    logger = get_logger("security")
    message = f"Security event: {event_type}"
    if user_id:
        message += f" by user {user_id}"
    if details:
        message += f" - Details: {details}"
    logger.warning(message)

def log_error(error: Exception, context: str = None) -> None:
    """Log error events with context"""
    logger = get_logger("errors")
    message = f"Error: {str(error)}"
    if context:
        message += f" - Context: {context}"
    logger.error(message, exc_info=True)