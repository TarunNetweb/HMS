from pydantic import BaseModel, computed_field, Field, EmailStr, validator
from fastapi import HTTPException,status
from datetime import date
#from typing import Optional

class EmployeeBase(BaseModel):
    salutation: str = Field(...,min_length=1)
    first_name: str = Field(...,min_length=1)
    last_name: str = Field(...,min_length=1)
    date_of_birth: date = Field(...)
    phone: str = Field(min_length = 10,max_length = 10)
    emergency_contact: str = Field(min_length = 10,max_length = 10)
    email: EmailStr = Field(...,min_length=1)
    password: str = Field(...,min_length=1)
    gender: str = Field(...,min_length=1)
    address: str = Field(...,min_length=10)
    city: str=Field(...,min_length=1)
    state: str = Field(...,min_length=1)
    pincode: str = Field(...,min_length=6,max_length=6)
    role: str = Field(...,min_length=1)
    qualification: str = Field(...,min_length=1)
    department: str = Field(...,min_length=1)
    bio: str | None = None
    
    @validator('password')
    def validatePassword(cls,v):
        passWord = v
        if len(passWord) <8:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Password should be 8 characters long")
        if any(c.isupper() for c in passWord) == False:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Password should contain atleast 1 uppercase letter")
        if any(c.islower() for c in passWord) == False:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Password should contain atleast 1 lowercase letter")
        if any(c.isdigit() for c in passWord) == False:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Password should contain atleast 1 numeric character")
        if any(not c.isalnum() and c not in (' ','\t','\n','=','%') for c in passWord) == False:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Password should contain atleast 1 special character")
        return passWord
    
    @computed_field
    @property
    def age(self) -> int:
        today = date.today()
        age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return age
    
class EmployeeCreate(EmployeeBase):
    confirm_password: str = Field(...,min_length=1)
    
    @validator('confirm_password')
    def validateConfirmPassword(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Confirm Password doesn't match")
        return v

class EmployeeUpdate(EmployeeBase):
    password: str = Field(...,min_length=1)
        
class EmployeeLogin(BaseModel):
    username: EmailStr
    password: str