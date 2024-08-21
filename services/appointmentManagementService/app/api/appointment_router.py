from fastapi import APIRouter, HTTPException, Request, Depends, status, Header
from app.schemas.models import AppointmentCreate,AppointmentUpdate
from app.repository import appointmentRepository as appointmentRepo
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

def Check_Authorization(Authorization: str = Header(None)):
    if not Authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header missing")
    
    token = Authorization.split(" ")[1] if Authorization.startswith("Bearer ") else None
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{auth_url}/validateTokenPatient", headers=headers)

    return response

def Check_Authorization_Admin(Authorization: str = Header(None)):
    if not Authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header missing")
    
    token = Authorization.split(" ")[1] if Authorization.startswith("Bearer ") else None
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{auth_url}/validateTokenAdmin", headers=headers)

    return response

@router.post("/book")
def CreateNewAppointment(new_appointment: AppointmentCreate, db: Session = Depends(get_db),Authorization:str = Header(None)):
    is_Authorized = Check_Authorization(Authorization=Authorization)
    
    if is_Authorized.status_code != 200:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorizaed access !")
    
    appointmentRepo.create_appointment(new_appointment=new_appointment,db=db)
    appointments = appointmentRepo.get_appointment_details(patient_id=new_appointment.patient_id,db=db)
    return {"msg":"Booked !!","appointments":appointments}

@router.get("/patient/{patient_id:int}")
def GetPatientAppointment(patient_id: int, Authorization:str = Header(None), db: Session = Depends(get_db)):
    is_Authorized = Check_Authorization(Authorization=Authorization)
    
    if is_Authorized.status_code != 200:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorizaed access !")
    
    appointments = appointmentRepo.get_appointment_details(patient_id=patient_id,db=db)
    return appointments

@router.get("/patient/{patient_id:int}/appointment/{appointment_id:int}")
def GetAppointmentForPatient(patient_id: int,appointment_id: int,str = Header(None), db: Session = Depends(get_db), Authorization:str = Header(None)):
    is_Authorized = Check_Authorization(Authorization=Authorization)
    
    if is_Authorized.status_code != 200:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorizaed access !")
    
    appointment = appointmentRepo.get_appointment(patient_id=patient_id,appointment_id=appointment_id,db=db)
    return appointment
    pass

@router.put("/{appointment_id:int}/cancel")
def CancelAppointment(appointment_id: int,db:Session = Depends(get_db),Authorization:str = Header(None)):
    is_Authorized = Check_Authorization(Authorization=Authorization)
    
    if is_Authorized.status_code != 200:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorizaed access !")
    
    message = appointmentRepo.cancel_appointment(appointment_id=appointment_id,db=db)
    return message

@router.put("/{appointment_id:int}/accept")
def ApproveAppointment(appointment_id: int,db:Session = Depends(get_db),Authorization:str = Header(None)):
    is_Authorized = Check_Authorization(Authorization=Authorization)

    if is_Authorized.status_code != 200:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorizaed access !")
    
    message = appointmentRepo.approved_appointment(appointment_id=appointment_id,db=db)
    return message

@router.put("/{appointment_id:int}/complete")
def ApproveAppointment(appointment_id: int,db:Session = Depends(get_db),Authorization:str = Header(None)):
    is_Authorized = Check_Authorization(Authorization=Authorization)

    if is_Authorized.status_code != 200:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorizaed access !")
    
    message = appointmentRepo.complete_appointment(appointment_id=appointment_id,db=db)
    return message

@router.patch("/{appointment_id:int}/reschedule")
def ApproveAppointment(appointment_id: int,update_details: AppointmentUpdate,db:Session = Depends(get_db),Authorization:str = Header(None)):
    is_Authorized = Check_Authorization(Authorization=Authorization)

    if is_Authorized.status_code != 200:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorizaed access !")
    
    message = appointmentRepo.reschedule_appointment(appointment_id=appointment_id,update_details = update_details,db=db)
    return message

@router.get("/doctor/{doctor_id:int}")
def GetPatientAppointment(doctor_id: int, Authorization:str = Header(None), db: Session = Depends(get_db)):
    is_Authorized = Check_Authorization(Authorization=Authorization)
    
    if is_Authorized.status_code != 200:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorizaed access !")
    
    appointments = appointmentRepo.get_appointment_details_doctors(doctor_id=doctor_id,db=db)
    return appointments

@router.get("/{appointment_id:int}")
def GetAppointment(appointment_id:int , Authorization:str = Header(None), db: Session= Depends(get_db)):
    is_Authorized = Check_Authorization(Authorization=Authorization)
    
    if is_Authorized.status_code != 200:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorizaed access !")
    
    appointment = appointmentRepo.get_appointment_by_id(appointment_id=appointment_id,db=db)
    return appointment

@router.get("/all")
def getAllAppointments( Authorization:str = Header(None), db: Session= Depends(get_db)):
    is_Authorized = Check_Authorization_Admin(Authorization=Authorization)
    
    if is_Authorized.status_code != 200:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorizaed access !")
    
    appointments = appointmentRepo.get_all_appointments(db=db)
    return appointments
