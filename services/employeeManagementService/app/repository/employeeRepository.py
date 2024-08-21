from sqlalchemy.orm import Session
from database.models import Employee, Patient
from app.schemas.models import EmployeeCreate, EmployeeUpdate

def get_employee(db: Session, employee_id: int):
    return db.query(Employee).filter(Employee.id == employee_id).first()

def get_all_employee(db: Session):
    return db.query(Employee).all()

def get_employee_email(db: Session, email_id: str):
    return db.query(Employee).filter(Employee.email == email_id).first()

def create_employee(db: Session, new_employee: EmployeeCreate):
    db_employee = Employee(
                        salutation = new_employee.salutation,
                        first_name = new_employee.first_name,
                        last_name = new_employee.last_name,
                        date_of_birth = new_employee.date_of_birth,
                        age = new_employee.age,
                        email = new_employee.email,
                        phone = new_employee.phone,
                        emergency_contact = new_employee.emergency_contact,
                        gender = new_employee.gender,
                        address = new_employee.address,
                        city = new_employee.city,
                        state= new_employee.state,
                        pincode = new_employee.pincode,
                        role = new_employee.role,
                        qualification = new_employee.qualification,
                        department = new_employee.department,
                        bio = new_employee.bio)
    
    db_employee.set_password(new_employee.password),
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return {"msg":"Employee Registration Successful"}

def update_employee(db: Session, update_employee: EmployeeUpdate, employee_id: int):
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
            
    if (db_employee.check_password(update_employee.password) == False):
        return {"message": "Wrong password"}
    
    
    db_employee.salutation = update_employee.salutation
    db_employee.first_name = update_employee.first_name
    db_employee.last_name = update_employee.last_name
    db_employee.date_of_birth = update_employee.date_of_birth
    db_employee.age = update_employee.age
    db_employee.email = update_employee.email
    db_employee.phone = update_employee.phone
    db_employee.emergency_contact = update_employee.emergency_contact
    db_employee.gender = update_employee.gender
    db_employee.address = update_employee.address
    db_employee.city = update_employee.city
    db_employee.state= update_employee.state
    db_employee.pincode = update_employee.pincode
    db_employee.role = update_employee.role
    db_employee.qualification = update_employee.qualification
    db_employee.department = update_employee.department
    db_employee.bio = update_employee.bio
    
    db.commit()
    db.refresh(db_employee)
    return db_employee