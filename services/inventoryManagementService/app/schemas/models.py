from pydantic import BaseModel, computed_field, Field, EmailStr, validator
from fastapi import HTTPException,status
from datetime import date

from typing import Optional

#from typing import Optional

class InventoryBase(BaseModel):
    name_of_equipment: str = Field(...,min_length=1)
    category_of_equipment: str = Field(...,min_length=1)
    stock_of_equipment: int = Field(...)
    unit_price: int = Field(...)
    date_of_purchase: date = Field(...)

class InventoryUpdate(BaseModel):
    stock_of_equipment: Optional[int] = None
    unit_price: Optional[int] = None
    