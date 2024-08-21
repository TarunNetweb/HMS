from fastapi import APIRouter, HTTPException, Depends, status, Header
from app.schemas.models import EmployeeCreate, EmployeeUpdate
from app.repository import employeeRepository as EmployeeRepo 
from database.databaseconnection import SessionLocal
from sqlalchemy.orm import Session
import requests
import json

router = APIRouter()
auth_url = "http://192.168.0.135:5000/authentication"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def Check_AuthorizationAdmin(Authorization: str = Header(None)):
    if not Authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header missing")
    
    token = Authorization.split(" ")[1] if Authorization.startswith("Bearer ") else None
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{auth_url}/validateTokenAdmin", headers=headers)

    return response

def Check_AuthorizationStaff(Authorization: str = Header(None)):
    if not Authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header missing")
    
    token = Authorization.split(" ")[1] if Authorization.startswith("Bearer ") else None
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{auth_url}/validateTokenStaff", headers=headers)

    return response

# NOTE Get all the employees
@router.get("/all")
async def GetAllEmployees(Authorization: str = Header(None),db:Session = Depends(get_db)):
    is_Authorized = Check_AuthorizationAdmin(Authorization=Authorization)
    
    if is_Authorized.status_code != 200:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorizaed access !")
    
    employees = EmployeeRepo.get_all_employee(db=db)
    return employees


@router.get("/me")
async def EmployeeInformation(Authorization: str = Header(None),db: Session = Depends(get_db)):
    is_Authorized = Check_AuthorizationAdmin(Authorization=Authorization)
    
    if is_Authorized.status_code != 200:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorizaed access !")
    
    userfromDb = EmployeeRepo.get_employee_email(email_id=is_Authorized.json()['username'],db=db)
    
    return userfromDb

# NOTE Get employee based on employee_id
@router.get("/{employee_id}")
async def GetEmployee(employee_id: int, db: Session = Depends(get_db)):
    employee = EmployeeRepo.get_employee(employee_id=employee_id,db=db)
    return employee

@router.patch("/{employee_id}")
async def GetEmployee(employee_id: int, update_employee: EmployeeUpdate, Authorization: str = Header(None),db: Session = Depends(get_db)):
    is_Authorized_Admin = Check_AuthorizationAdmin(Authorization=Authorization)
    is_Authorized_Staff = Check_AuthorizationStaff(Authorization=Authorization)
    
    if is_Authorized_Admin.status_code == 200 or is_Authorized_Staff.status_code == 200:
        employee = EmployeeRepo.update_employee(employee_id=employee_id,update_employee=update_employee,db=db)
        return employee
    
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorizaed access !")

# NOTE Employee registration
@router.post('/registration')
async def EmployeeRegistration(new_employee: EmployeeCreate, Authorization: str = Header(None),db: Session = Depends(get_db)):
    is_Authorized = Check_AuthorizationAdmin(Authorization=Authorization)
    
    if is_Authorized.status_code != 200:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorizaed access !")
    
    employeefromDb = EmployeeRepo.get_employee_email(email_id = new_employee.email, db = db)
    
    if employeefromDb:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Employee already exists in the database")
    try:
        return EmployeeRepo.create_employee(db=db, new_employee=new_employee)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Something went wrong !!")