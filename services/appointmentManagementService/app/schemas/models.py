from pydantic import BaseModel, Field, computed_field,validator
from fastapi import HTTPException,status
from datetime import datetime,date,time 

# NOTE - Appointment Create Model
class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    date: date 
    time: str
    description: str = Field(...,min_length=1)
    
    @validator('time')
    def validateConfirmPassword(cls, v):
        try:
            datetime.strptime(v, "%I:%M %p")
            return v  
        except ValueError:
             raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Invalid time format !!",
                            headers={"WWW-Authenticate": "Bearer"})

# NOTE Appointment from Database model
class AppointmentFromDb(BaseModel):
    id:int
    patient_name: str
    doctor_name: str
    date: date
    time: str
    description: str
    status: str
    doctor_id: int
    patient_id: int
    
    @computed_field
    @property
    def time_12(self) -> str:
        # Parse the 24-hour time string into a datetime object
        time_obj = datetime.strptime(self.time, '%H:%M:%S')
    
        # Format the datetime object into a 12-hour format string
        time_str_12 = time_obj.strftime('%I:%M %p')
        return f"{time_str_12}"
    
class AppointmentUpdate(BaseModel):
    date: date
    time: str
    description: str
    
    @computed_field
    @property
    def time_12(self) -> str:
        # Parse the 24-hour time string into a datetime object
        time_obj = datetime.strptime(self.time, '%H:%M:%S')
    
        # Format the datetime object into a 12-hour format string
        time_str_12 = time_obj.strftime('%I:%M %p')
        return f"{time_str_12}"