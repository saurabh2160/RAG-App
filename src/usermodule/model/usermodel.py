from pydantic import BaseModel, EmailStr

class UserSchema(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

class UserCreateResponse(BaseModel):
    message: str
    token: str

class UserLoginResponse(BaseModel):
    message: str
    token: str
