from pydantic import BaseModel
from typing import Optional
from models.user import UserResponse

class LoginRequest(BaseModel):
    email: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securePassword123!"
            }
        }

class LoginResponse(BaseModel):
    user: UserResponse
    token: str

    class Config:
        json_schema_extra = {
            "example": {
                "user": {
                    "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
                    "email": "user@example.com",
                    "created_at": "2026-01-04T10:30:00Z"
                },
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
        }