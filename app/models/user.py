from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


class CreateUser(BaseModel):
    email: str = Field(...)
    password: str = Field(...)
    name: str = Field(...)

class UserSignUp(BaseModel):
    name: str
    email: EmailStr
    password: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    is_deleted: bool = Field(default=False)

class UserAuth(BaseModel):
    email: str = Field(...)
    password: str = Field(...)