from pydantic import BaseModel, computed_field, Field, EmailStr, validator
from fastapi import HTTPException,status
from datetime import date

from typing import Optional

class TypeOfMedicalReport(BaseModel):
    required_report: str = Field(...,min_length=1)


    
class MedicalReportBase(BaseModel):
    chief_complaint: str = Field(...,min_length=1)
    history_of_present_illness: str = Field(...,min_length=1)
    past_medical_history: str = Field(...)
    medication_history: str = Field(...)
    family_history: str = Field(...)
    social_history: str = Field(...)
    review_of_systems: str = Field(...)
    physical_exam_findings: str = Field(...)
    blood_report_id: Optional[int] = None
    appointment_id: Optional[int] = None
    wbc_count : Optional[float] = None
    rbc_count : Optional[float] = None
    hemoglobin : Optional[float] = None
    hematocrit : Optional[float] = None
    mean_corpuscular_volume : Optional[float] = None
    mean_corpuscular_hemoglobin : Optional[float] = None
    mean_corpuscular_hemoglobin_concentration : Optional[float] = None
    platelet_count : Optional[float] = None 
    neutrophils : Optional[float] = None
    monocytes : Optional[float] = None
    lymphocytes : Optional[float] = None
    eosinophils : Optional[float] = None
    basophils : Optional[float] = None
    glucose : Optional[float] = None
    sodium: Optional[float] = None
    potassium : Optional[float] = None
    chloride : Optional[float] = None
    bicarbonate : Optional[float] = None
    ast: Optional[float] = None
    alp : Optional[float] = None
    alt : Optional[float] = None
    bilirubin: Optional[float] = None
    creatinine : Optional[float] = None
    bun : Optional[float] = None
    total_cholesterol : Optional[float] = None
    good_cholesterol : Optional[float] = None
    bad_cholesterol : Optional[float] = None
    triglycerides : Optional[float] = None
    prothrombin_time : Optional[float] = None
    partial_thrombin_time: Optional[float] = None
    international_normalized_ratio : Optional[float] = None
