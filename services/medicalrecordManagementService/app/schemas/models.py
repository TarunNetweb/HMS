from pydantic import BaseModel, Field, computed_field,validator
from fastapi import HTTPException,status
from datetime import datetime,date,time 


class MedicalRecordCreate(BaseModel):
    prescriptions: str
    advise: str
    date_of_record: date
    billing: int
    appointment_id: int
