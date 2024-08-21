from fastapi import APIRouter, HTTPException, Request, Depends, status, Header
#from app.schemas.models import EmployeeCreate,EmployeeLogin
from app.repository import doctorsRepository as DoctorRepo
from database.databaseconnection import SessionLocal
from app.schemas.doctorModels import AppointmentAvailability
from sqlalchemy.orm import Session
import requests

router = APIRouter()
auth_url = "http://192.168.0.135:5000/authentication"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
def Check_Authorization(Authorization: str = Header(None)):
    if not Authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header missing")
    
    token = Authorization.split(" ")[1] if Authorization.startswith("Bearer ") else None
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{auth_url}/validateTokenStaff", headers=headers)

    return response
        
@router.get("/category/{category}")
def getAllCategories(category, db:Session = Depends(get_db)):
    doctors = DoctorRepo.get_doctor_category(category = category, db = db)
    return doctors

@router.get("/doctors")
def getAllDoctors(db: Session = Depends(get_db)):
    doctors = DoctorRepo.get_doctors(db=db)
    return doctors

@router.get("/{doctor_id}/slots")
def getDoctorSlots(doctor_id: int, db: Session = Depends(get_db)):
    doctor_slots = DoctorRepo.get_doctor_slots(db=db,doctor_id=doctor_id)
    return doctor_slots

@router.get("/{doctor_id}/patients")
def getDoctorPatientss(doctor_id: int,Authorization: str = Header(None), db: Session = Depends(get_db)):
    is_Authorized = Check_Authorization(Authorization=Authorization)
    
    if is_Authorized.status_code != 200:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorizaed access !")
    
    patients_of_doctor = DoctorRepo.get_doctor_patients(db=db,doctor_id=doctor_id)
    return patients_of_doctor

@router.post("/checkavailability")
def checkavailability(appointment: AppointmentAvailability, db: Session = Depends(get_db)):
    print(appointment)
    is_available = DoctorRepo.check_doctor_availability(appointment=appointment,db=db)
    return is_available

@router.get("/me")
async def DoctorInformation(Authorization: str = Header(None),db: Session = Depends(get_db)):
    is_Authorized = Check_Authorization(Authorization=Authorization)
    
    if is_Authorized.status_code != 200:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorizaed access !")
    
    userfromDb = DoctorRepo.get_doctor_email(email_id=is_Authorized.json()['username'],db=db)
    
    return userfromDb