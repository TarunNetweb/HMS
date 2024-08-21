from sqlalchemy.orm import Session
from database.models import Patient
from app.schemas.models import PatientCreate, PatientUpdate

def get_patient(db: Session, patient_id: int):
    return db.query(Patient).filter(Patient.id == patient_id).first()

def get_patient_email(db: Session, email_id: str):
    return db.query(Patient).filter(Patient.email == email_id).first()

def get_all(db:Session):
    return db.query(Patient).all()

def create_patient(db: Session, new_patient: PatientCreate):
    db_patient = Patient(first_name = new_patient.first_name,
                        last_name = new_patient.last_name,
                        date_of_birth = new_patient.date_of_birth,
                        age = new_patient.age,
                        email = new_patient.email,
                        phone = new_patient.phone,
                        emergency_contact = new_patient.emergency_contact,
                        tnc = new_patient.tnc,
                        height = new_patient.height,
                        weight = new_patient.weight,
                        blood_type = new_patient.blood_type,
                        gender = new_patient.gender,
                        address = new_patient.address,
                        city = new_patient.city,
                        state= new_patient.state,
                        pincode = new_patient.pincode)
    
    db_patient.set_password(new_patient.password)
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return {"msg":"Registration Successful"}

def update_patient(db: Session, patient_id: int, updated_patient: PatientUpdate):
    db_patient = db.query(Patient).filter(Patient.id == patient_id).first()
    print("Db patient",db_patient)
    print("update patient",updated_patient)
            
    if (db_patient.check_password(updated_patient.password) == False):
        return {"message": "wrong password you entered, click on forgot password"}
   
    db_patient.first_name = updated_patient.first_name
    db_patient.last_name = updated_patient.last_name
    db_patient.date_of_birth = updated_patient.date_of_birth
    db_patient.email = updated_patient.email
    db_patient.phone = updated_patient.phone
    db_patient.emergency_contact = updated_patient.emergency_contact
    db_patient.height = updated_patient.height
    db_patient.weight = updated_patient.weight
    db_patient.blood_type = updated_patient.blood_type
    db_patient.address = updated_patient.address
    db_patient.city = updated_patient.city
    db_patient.state = updated_patient.state
    db_patient.pincode = updated_patient.pincode
    db_patient.gender = updated_patient.gender
    
    db.commit()
    db.refresh(db_patient)
    return db_patient
