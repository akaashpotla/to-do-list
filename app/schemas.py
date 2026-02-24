import re
from pydantic import BaseModel, EmailStr, Field, field_validator
from app.core.enums import TaskStatus

class User(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    email: EmailStr = Field(min_length=1, max_length=255)
    password: str = Field(min_length=8, max_length=30)
    
    @field_validator('password')
    def password_checker(cls, v):
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Password requires at least 1 special character")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password requires at least 1 uppercase character")
        if not re.search(r"\d", v):
            raise ValueError("Password requires at least 1 number")
        return v
    
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

class Task(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    
class TaskResponse(BaseModel):
    id: int
    title: str
    state: TaskStatus
    user_id: int

    class Config:
        from_attributes = True

class TokenData(BaseModel):
    email: str