from pydantic import BaseModel

class AdminCreate(BaseModel):
    username: str
    email: str
    password: str

class AdminInDB(BaseModel):
    username: str
    email: str
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str

class LoginRequest(BaseModel):
    username: str
    password: str




