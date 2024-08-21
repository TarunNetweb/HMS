import requests
from fastapi import APIRouter, HTTPException, Request, Depends, status, Header
from app.schemas.models import MedicalReportBase, TypeOfMedicalReport
from app.repository import reports_repository as ReportRepo
from database.databaseconnection import SessionLocal
from sqlalchemy.orm import Session

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

@router.get("/reports/{patient_id}")
async def getAllReports(patient_id: int ,Authorization: str = Header(None), db:Session = Depends(get_db)):
    is_Authorized = Check_Authorization(Authorization=Authorization)
    
    if is_Authorized.status_code != 200:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorizaed access !")
    
    Reports_of_Patient =  ReportRepo.get_all_reports_of_patient(db=db, patient=patient_id)
    try:
        return Reports_of_Patient
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Something went wrong !!")

@router.get("/reports")
async def getAllReports(Authorization: str = Header(None), db:Session = Depends(get_db)):
    is_Authorized = Check_Authorization(Authorization=Authorization)
    
    if is_Authorized.status_code != 200:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorizaed access !")
    
    Reports_of_Patient =  ReportRepo.get_all_reports(db=db)
    try:
        return Reports_of_Patient
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Something went wrong !!")


@router.post("/reports/specific/{patient_id}/{report_id}")
async def getAllReports(patient_id: int , type_of_report : TypeOfMedicalReport,report_id :  int, Authorization: str = Header(None),db:Session = Depends(get_db)):
    is_Authorized = Check_Authorization(Authorization=Authorization)
    
    if is_Authorized.status_code != 200:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorizaed access !")
    
    Reports_of_Patient =  ReportRepo.get_specific_report_of_patient(db=db, report_id= report_id, type_of_report=type_of_report)
    try:
        return Reports_of_Patient
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Something went wrong !!")


@router.post("/create")
async def makeNewStock(newMedicalReportBase:MedicalReportBase,Authorization: str = Header(None), db:Session = Depends(get_db)):
    is_Authorized = Check_Authorization(Authorization=Authorization)
    
    if is_Authorized.status_code != 200:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorizaed access !")
    
    Reports = ReportRepo.get_medical_report(db=db, medical_report_id= newMedicalReportBase.appointment_id)
    if Reports:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Report already exists in the database")
    try:
        return ReportRepo.create_new_medical_report(db=db, new_medical_report= newMedicalReportBase)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Something went wrong !!")
