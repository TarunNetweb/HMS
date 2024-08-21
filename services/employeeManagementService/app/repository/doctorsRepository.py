from sqlalchemy.orm import Session
from database.models import Employee,AppointmentSlots, Appointment, Patient
from app.schemas.doctorModels import AppointmentSlotsModel, AppointmentAvailability
from datetime import datetime
import pytz
from fastapi import HTTPException, status

def get_doctor_email(db: Session, email_id: str):
    return db.query(Employee).filter(Employee.email == email_id).first()

# NOTE Get the category of a doctor
def get_doctor_category(db: Session, category: str):
    doctors = db.query(Employee).filter(Employee.department == category).all()
    return doctors

# NOTE Get all the doctors
def get_doctors(db: Session):
    doctors = db.query(Employee).filter(Employee.role == "Doctor").all()
    return doctors

# NOTE Get doctor slots
def get_doctor_slots(db: Session,doctor_id: int):
    available_slots = db.query(AppointmentSlots).filter(AppointmentSlots.doctor_id == doctor_id).all()
    final_slots = []
    for slot in available_slots:
        print(slot)
        final_slot = AppointmentSlotsModel.from_orm(slot)
        final_slots.append(final_slot)
    return final_slots

def get_doctor_patients(db:Session,doctor_id: int):
    patients = db.query(Patient).join(Appointment, Appointment.patient_id == Patient.id).filter(Appointment.doctor_id == doctor_id).all()
    
    return patients

# NOTE Check doctor availability
def check_doctor_availability(db: Session,appointment: AppointmentAvailability ):
    booked_appointments = db.query(AppointmentSlots).filter(
        AppointmentSlots.doctor_id == appointment.doctor_id,
        ~db.query(Appointment).filter(Appointment.doctor_id == appointment.doctor_id,
                                     Appointment.date == appointment.date,
                                     Appointment.time_slot == AppointmentSlots.slot_start).exists()).all()
    current_time = datetime.now(pytz.timezone("Asia/Kolkata")).time()  # Get current time as a datetime.time object
    
    current_date = datetime.now().date()
    
    booked_slots = []
    print(current_time)
    for appointments in booked_appointments:
        slot_start_time = appointments.slot_start  # Assuming this is a datetime.time object

        # Compare times directly without converting to string
        
        if current_date<appointment.date:
            slot_display = slot_start_time.strftime("%I:%M %p")
            booked_slots.append({"id": appointments.id, "slot": slot_display})
        elif slot_start_time > current_time:
            # Now format the slot_start_time for display purposes
            slot_display = slot_start_time.strftime("%I:%M %p")
            booked_slots.append({"id": appointments.id, "slot": slot_display})
        
    print(booked_slots)

    return booked_slots