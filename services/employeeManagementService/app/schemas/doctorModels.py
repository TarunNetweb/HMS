from pydantic import BaseModel, validator, computed_field
from datetime import datetime,date

class AppointmentSlotsModel(BaseModel):
    id: int
    slot_start: datetime
    slot_end: datetime

    @computed_field
    @property
    def slot(self) -> str:
        return f"{self.slotStart.strftime('%H:%M')} - {self.slotEnd.strftime('%H:%M')}"
    
    class Config:
        from_attributes = True
        
class AppointmentAvailability(BaseModel):
    date: date
    doctor_id: int
        