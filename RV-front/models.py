from pydantic import BaseModel, Field, field_validator, EmailStr
from typing import Optional
import re

class UserSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=8)
    password_confirmation: str = Field(...)
    
    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        if not re.match("^[a-zA-Z0-9_.-]+$", v):
            raise ValueError('Username can only contain letters, numbers, dots, underscores and hyphens')
        return v
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r"[A-Z]", v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r"[a-z]", v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r"\d", v):
            raise ValueError('Password must contain at least one digit')
        return v
    
    @field_validator('password_confirmation')
    @classmethod
    def passwords_match(cls, v, info):
        if 'password' in info.data and v != info.data['password']:
            raise ValueError('Passwords do not match')
        return v

class UserInDB(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class PredictionSchema(BaseModel):
    filename: str
    content_type: str
    disease: str
    user_id: Optional[str] = None