from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from app.schemas.models import UserCreds
from database.models import Patient, Employee

# NOTE To check if the user exists or not before generating the token and assign the role
def authenticate_user(db: Session, creds: UserCreds):
    patientFromDb = db.query(Patient).filter(Patient.email == creds.username).first()
    employeeFromDb = db.query(Employee).filter(Employee.email == creds.username).first()
    
    if patientFromDb == None and employeeFromDb == None :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="User doesn't exists",
                            headers={"WWW-Authenticate": "Bearer"})
    elif patientFromDb != None and employeeFromDb == None and patientFromDb.check_password(creds.password):
        return "Patient"
    elif employeeFromDb != None and patientFromDb == None and employeeFromDb.check_password(creds.password):
        return employeeFromDb.role
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})

# NOTE To check if the user exists or not before generating the token and assign the role
def authorized_patient(db: Session, username, role):
    patientFromDb = db.query(Patient).filter(Patient.email == username).first()
    
    if patientFromDb != None and role=="Patient":
        print("Patient")
        return patientFromDb
    return False

def authorized_employee(username,db:Session):
    employeeFromDb = db.query(Employee).filter(Employee.email == username).first()

    if employeeFromDb!=None:
        print("Employee")
        return employeeFromDb
    return False

def authorized_admin(username,db:Session):
    adminFromDb = db.query(Employee).filter(Employee.email == username).first()

    if adminFromDb!=None:
        return adminFromDb
    return False