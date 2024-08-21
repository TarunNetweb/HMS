from sqlalchemy.orm import Session
from database.models import Appointment, Employee, Patient
from datetime import date,datetime
from app.schemas.models import AppointmentCreate, AppointmentFromDb, AppointmentUpdate


def get_all_appointments(db: Session):
    appointment = db.query(Appointment).filter().all()
    return appointment

def get_appointment(patient_id: int, appointment_id: int,db: Session):
    appointment = db.query(Appointment).join(Patient, Patient.id == Appointment.patient_id).join(Employee, Employee.id == Appointment.doctor_id).filter(Appointment.patient_id == patient_id,Appointment.id==appointment_id).first()
    
    if appointment:
        detail = AppointmentFromDb(
            id=appointment.id,
            doctor_id = (appointment.doctor.id),
            patient_id = (appointment.patient.id),
            patient_name=(appointment.patient.first_name+" "+appointment.patient.last_name),
            doctor_name=(appointment.doctor.first_name+" "+appointment.doctor.last_name),
            date=appointment.date,
            time=appointment.time_slot,
            description=appointment.description,
            status=appointment.status
        )
        return detail
    return []

def get_appointment_details(db: Session, patient_id: int) -> AppointmentFromDb:
    appointments = db.query(Appointment).join(Patient, Patient.id == Appointment.patient_id).join(Employee, Employee.id == Appointment.doctor_id).filter(Appointment.patient_id == patient_id).all()
    
    appointment_details = []
    for appointment in appointments:
        detail = AppointmentFromDb(
            id=appointment.id,
            doctor_id = (appointment.doctor.id),
            patient_id = (appointment.patient.id),
            patient_name=(appointment.patient.first_name+" "+appointment.patient.last_name),
            doctor_name=(appointment.doctor.first_name+" "+appointment.doctor.last_name),
            date=appointment.date,
            time=appointment.time_slot,
            description=appointment.description,
            status=appointment.status
        )
        appointment_details.append(detail)

    return appointment_details

def get_appointment_details_doctors(db: Session, doctor_id: int) -> AppointmentFromDb:
    appointments = db.query(Appointment).join(Employee, Employee.id == Appointment.doctor_id).join(Patient, Patient.id == Appointment.patient_id).filter(Appointment.doctor_id == doctor_id).all()
    
    appointment_details = []
    for appointment in appointments:
        detail = AppointmentFromDb(
            id=appointment.id,
            doctor_id = (appointment.doctor.id),
            patient_id = (appointment.patient.id),
            doctor_name=(appointment.doctor.first_name+" "+appointment.doctor.last_name),
            patient_name=(appointment.patient.first_name+" "+appointment.patient.last_name),
            date=appointment.date,
            time=appointment.time_slot,
            description=appointment.description,
            status=appointment.status
        )
        appointment_details.append(detail)

    return appointment_details

def create_appointment(db: Session, new_appointment: AppointmentCreate):
    time_object = datetime.strptime(new_appointment.time, "%I:%M %p")
    time_in_24_hour_format = time_object.strftime("%H:%M:%S")
    db_appointment = Appointment(date = new_appointment.date,
                        time_slot = time_in_24_hour_format,
                        description= new_appointment.description,
                        patient_id = new_appointment.patient_id,
                        doctor_id = new_appointment.doctor_id,
                        status = "pending")
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return {"msg":"Appointment Booked"}

def reschedule_appointment(db: Session, update_details: AppointmentUpdate,appointment_id:int):
    time_object = datetime.strptime(update_details.time, "%I:%M %p")
    time_in_24_hour_format = time_object.strftime("%H:%M:%S")
    
    db_appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    
    db_appointment.time = time_in_24_hour_format
    db_appointment.description = update_details.description
    db_appointment.date = update_details.date
    db_appointment.status = "upcoming"
    
    db.commit()
    db.refresh(db_appointment)
    return {"msg":"Appointment Rescheduled"}

def cancel_appointment(db:Session,appointment_id: int):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    appointment.status = "cancelled"
    
    db.commit()
    db.refresh(appointment)
    return {"msg":"Appointment Cancelled"}
    
def approved_appointment(db:Session,appointment_id: int):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    appointment.status = ""
    
    db.commit()
    db.refresh(appointment)
    return {"msg":"Appointment approved"}

def completed_appointment(db:Session,appointment_id: int):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    appointment.status = "completed"
    
    db.commit()
    db.refresh(appointment)
    return {"msg":"Appointment Completed"}

def get_appointment_by_id(appointment_id,db:Session) -> AppointmentFromDb:
    appointment = db.query(Appointment).join(Employee, Employee.id == Appointment.doctor_id).join(Patient, Patient.id == Appointment.patient_id).filter(Appointment.id == appointment_id).first()
    
    appointment_details = AppointmentFromDb(
            id=appointment.id,
            doctor_id = (appointment.doctor.id),
            patient_id = (appointment.patient.id),
            doctor_name=(appointment.doctor.first_name+" "+appointment.doctor.last_name),
            patient_name=(appointment.patient.first_name+" "+appointment.patient.last_name),
            date=appointment.date,
            time=appointment.time_slot,
            description=appointment.description,
            status=appointment.status
        )
    return appointment_details