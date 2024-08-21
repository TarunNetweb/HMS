from pydantic import BaseModel, computed_field, Field, EmailStr, validator
from fastapi import HTTPException,status
from datetime import date
from typing import Optional

class PatientBase(BaseModel):
    first_name: str = Field(...,min_length=1)
    last_name: str = Field(...,min_length=1)
    date_of_birth: date = Field(...)
    phone: str = Field(min_length = 10,max_length = 10)
    emergency_contact: str = Field(min_length = 10,max_length = 10)
    email: EmailStr = Field(...,min_length=1)
    password: str = Field(...,min_length=1)
    blood_type: str = Field(...,min_lenth=1)
    height: float | None = None
    weight: float | None = None
    tnc: bool = Field(...)
    gender: str = Field(...,min_length=1)
    address: str = Field(...,min_length=10)
    city: str=Field(...,min_length=1)
    state: str = Field(...,min_length=1)
    pincode: str = Field(...,min_length=6,max_length=6)
    
    @validator('password')
    def validatePassword(cls,v):
        passWord = v
        if len(passWord) <8:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Password should be 8 characters long",
                            headers={"WWW-Authenticate": "Bearer"})
        if any(c.isupper() for c in passWord) == False:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Password should contain atleast 1 uppercase letter",
                            headers={"WWW-Authenticate": "Bearer"})
        if any(c.islower() for c in passWord) == False:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Password should contain atleast 1 lowercase letter",
                            headers={"WWW-Authenticate": "Bearer"})
        if any(c.isdigit() for c in passWord) == False:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Password should contain atleast 1 numeric character",
                            headers={"WWW-Authenticate": "Bearer"})
        if any(not c.isalnum() and c not in (' ','\t','\n','=','%') for c in passWord) == False:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Password should contain atleast 1 special character",
                            headers={"WWW-Authenticate": "Bearer"})
        return passWord
    
    @validator('tnc')
    def acceptTermAndConditions(cls, v):
        if v==False:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Please accept the Terms and Conditions",
                            headers={"WWW-Authenticate": "Bearer"})
        return v

    @computed_field
    @property
    def age(self) -> int:
        today = date.today()
        age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return age
    
class PatientCreate(PatientBase):
    confirm_password: str = Field(...,min_length=1)
    
    @validator('confirm_password')
    def validateConfirmPassword(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Confirm Password doesn't match",
                            headers={"WWW-Authenticate": "Bearer"})
        return v
    
class PatientUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1)
    last_name: Optional[str] = Field(None, min_length=1)
    date_of_birth: Optional[date] = None
    phone: Optional[str] = Field(None, min_length=10, max_length=10)
    emergency_contact: Optional[str] = Field(None, min_length=10, max_length=10)
    email: Optional[EmailStr] = Field(None, min_length=1)
    email_confirmed: Optional[bool] = None
    password: str = Field(...,min_length=1)
    blood_type: Optional[str] = Field(None, min_length=1)
    height: Optional[float] = None
    weight: Optional[float] = None
    tnc: Optional[bool] = None
    gender: Optional[str] = Field(None, min_length=1)
    address: Optional[str] = Field(None, min_length=10)
    city: Optional[str] = Field(None, min_length=1)
    state: Optional[str] = Field(None, min_length=1)
    pincode: Optional[str] = Field(None, min_length=6, max_length=6)
 
    @computed_field
    @property
    def age(self) -> int:
        today = date.today()
        age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return age

class PatientForDb(PatientBase):
    id: int
    
    # @computed_field
    # @property
    # def age(self) -> int:
    #     today = date.today()
    #     age = today.year - self.dateOfBirth.year - ((today.month, today.day) < (self.dateOfBirth.month, self.dateOfBirth.day))
    #     return age
    
    class Config:
        orm_mode: True
        
class PatientLogin(BaseModel):
    username: EmailStr
    password: str