from pydantic import BaseModel, Field
from typing import Optional

class LoginRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Username")
    password: str = Field(..., min_length=6, description="Password")
    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "johndoe",
                "password": "securepassword123"
            }
        }
    }
class signupRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Username")
    email: str = Field(..., max_length=100, description="Email")
    password: str = Field(..., min_length=6, description="Password")
    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "johndoe",
                "email": "johndoe@example.com",
                "password": "securepassword123"
            }
        }
    }
class signupResponse(BaseModel):
    message: str = Field(..., description="Signup confirmation message")

class TokenResponse(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration time in seconds")
