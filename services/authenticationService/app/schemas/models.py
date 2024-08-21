from pydantic import BaseModel, computed_field, Field, EmailStr, validator

class UserCreds(BaseModel):
    username: EmailStr
    password: str

class AuthenticateUser(BaseModel):
    email: EmailStr
    jwt: str