from fastapi import APIRouter, HTTPException, Depends, status, Header
from app.schemas.models import PatientCreate, PatientUpdate
from app.repository import patientRepository as PatientRepo 
from database.databaseconnection import SessionLocal
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

# NOTE Check authrization of the patient
def Check_Authorization(Authorization: str = Header(None)):
    if not Authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header missing")
    
    token = Authorization.split(" ")[1] if Authorization.startswith("Bearer ") else None
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{auth_url}/validateTokenPatient", headers=headers)

    return response

# NOTE Check authrization of the employee
def Check_Authorization_Staff(Authorization: str = Header(None)):
    if not Authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header missing")
    
    token = Authorization.split(" ")[1] if Authorization.startswith("Bearer ") else None
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{auth_url}/validateTokenStaff", headers=headers)

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

# NOTE Patient registration
@router.post('/registration')
async def PatientRegistration(new_patient: PatientCreate, db: Session = Depends(get_db)):
    userfromDb = PatientRepo.get_patient_email(email_id = new_patient.email, db = db)
    
    if userfromDb:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="User already exists")
    try:
        message = PatientRepo.create_patient(db=db, new_patient=new_patient)
        return message
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Something went wrong !!")

# NOTE Get Patient information
@router.get("/me")
async def PatientInformation(Authorization: str = Header(None),db: Session = Depends(get_db)):
    is_Authorized = Check_Authorization(Authorization=Authorization)
    if is_Authorized.status_code != 200:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorizaed access !")
    
    userfromDb = PatientRepo.get_patient_email(email_id=is_Authorized.json()['username'],db=db)
    return userfromDb

# NOTE Get all the patients only for admin and doctors
@router.get("/all")
async def AllPatientInformation(Authorization: str = Header(None),db:Session = Depends(get_db)):
    is_Authorized_Staff = Check_Authorization_Staff(Authorization = Authorization)
    is_Authorized_Admin = Check_Authorization_Admin(Authorization = Authorization)
    
    if is_Authorized_Admin.status_code != 200 and is_Authorized_Staff.status != 200:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorizaed access !")

    usersFromDb = PatientRepo.get_all(db=db);
    return usersFromDb

# NOTE Get Patient information using patient_id
@router.get("/{patient_id}")
async def PatientInformationBasedOnId(patient_id: int, Authorization: str = Header(None),db: Session = Depends(get_db)):
    is_Authorized_Staff = Check_Authorization_Staff(Authorization = Authorization)
    
    if is_Authorized_Staff.status_code != 200:
        is_Authorized_Admin = Check_Authorization_Admin(Authorization = Authorization)
        if is_Authorized_Admin.status_code != 200:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorizaed access !")
        
    userfromDb = PatientRepo.get_patient(patient_id=patient_id,db=db)
    return userfromDb

# NOTE Update Patient information using patient_id
@router.patch("/{patient_id}")
async def patientUpdation(patient_id: int, update_patient: PatientUpdate,  db: Session = Depends(get_db), Authorization: str = Header(None)):
    is_Authorized = Check_Authorization(Authorization= Authorization)
    
    if is_Authorized.status_code != 200:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorizaed access !")
    
    userFromDb = PatientRepo.get_patient(db = db, patient_id= patient_id)
    
    if not userFromDb:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User does not exists")
    
    updated_patient_info =  PatientRepo.update_patient(db = db,patient_id = patient_id,updated_patient=update_patient)
    return updated_patient_info