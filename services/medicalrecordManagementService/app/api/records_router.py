from fastapi import APIRouter, HTTPException, Request, Depends, status, Header
from app.schemas.models import MedicalRecordCreate
from app.repository import records_repository as RRP
from database.databaseconnection import SessionLocal
from sqlalchemy.orm import Session
from datetime import date
import requests

router = APIRouter()
auth_url = "http://192.168.0.135:5000/authentication"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def Check_Authorization_Staff(Authorization: str = Header(None)):
    if not Authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header missing")
    
    token = Authorization.split(" ")[1] if Authorization.startswith("Bearer ") else None
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{auth_url}/validateTokenStaff", headers=headers)

    return response


def Check_Authorization_Patient(Authorization: str = Header(None)):
    if not Authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header missing")
    
    token = Authorization.split(" ")[1] if Authorization.startswith("Bearer ") else None
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{auth_url}/validateTokenPatient", headers=headers)

    return response

@router.get("/patient/{patient_id:int}")
def fetchMedicalRecordforpatient(patient_id:int,db: Session = Depends(get_db),Authorization:str = Header(None)):

    is_Authorized = Check_Authorization_Patient(Authorization=Authorization)
    print("patient geting  ", is_Authorized)
    if is_Authorized.status_code != 200:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorizaed access !")
    try:
        return RRP.getMedicalRecord(db=db,patient_id=patient_id)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Something went wrong !!")
    
@router.get("/doctor/{doctor_id:int}")
def fetchMedicalRecordforpatient(doctor_id:int,db: Session = Depends(get_db),Authorization:str = Header(None)):

    is_Authorized = Check_Authorization_Staff(Authorization=Authorization)
    print("patient geting  ", is_Authorized)
    if is_Authorized.status_code != 200:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorizaed access !")
    try:
        return RRP.getMedicalRecordofDoctors(db=db,doctor_id=doctor_id)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Something went wrong !!")
# getMedicalRecordofDoctors

@router.post("/create")
def createMedicalRecord(new_medical_record: MedicalRecordCreate, db: Session = Depends(get_db),Authorization:str = Header(None)):
    print(Authorization)
    is_Authorized = Check_Authorization_Staff(Authorization=Authorization)
    print("ssgfdjsfjdfgvjd ", is_Authorized)
    if is_Authorized.status_code != 200:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorizaed access !")
    earlier_record = RRP.getMedicalRecordbyAppointmentID(db=db, appointment_id=new_medical_record.appointment_id)
    if earlier_record:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="record is already there ")
    try:
        return RRP.createMedicalRecord(db=db, new_medical_record=new_medical_record)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Something went wrong !!")
