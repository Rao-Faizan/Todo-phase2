from fastapi import HTTPException, Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Any
from utils.jwt import verify_token
from uuid import UUID

security = HTTPBearer()

def validate_user_id(user_id: UUID, token_data: Dict[str, Any]) -> bool:
    """
    Validates that the user_id in the path matches the user_id in the JWT token
    """
    # Extract user ID from token (stored in 'sub' field)
    token_user_id = token_data.get("sub")

    # Compare the path user_id with the token user_id
    return str(user_id) == token_user_id

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """
    Dependency to get current user from JWT token
    """
    token = credentials.credentials

    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload

def verify_user_owns_resource(user_id: UUID, token_data: Dict[str, Any]) -> bool:
    """
    Verifies that the authenticated user owns the resource they're trying to access
    """
    return validate_user_id(user_id, token_data)