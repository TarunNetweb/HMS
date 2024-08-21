from sqlalchemy.orm import Session
from database.models import MedicalRecords, Appointment, Employee, Patient
from datetime import date,datetime
from app.schemas.models import MedicalRecordCreate
def createMedicalRecord(db: Session, new_medical_record: MedicalRecordCreate):
    Created_Medical_Record = MedicalRecords(
    prescriptions  = new_medical_record.prescriptions, 
    advise = new_medical_record.advise,
    billing =new_medical_record.billing,
    date_of_record = new_medical_record.date_of_record,
    appointment_id = new_medical_record.appointment_id,
    )

    db.add(Created_Medical_Record)
    db.commit()
    db.refresh(Created_Medical_Record)
    doctor_id = Created_Medical_Record.appointment.doctor_id
    print(" doctor's id", doctor_id)
    
    medicalRecords = db.query(MedicalRecords).filter().all()
    medical_records = (
        db.query(MedicalRecords)
        .join(Appointment, Appointment.id == MedicalRecords.appointment_id)
        .join(Patient, Patient.id == Appointment.patient_id)
        .filter(Appointment.doctor_id == doctor_id)
        .all()
    )

    records_with_appointment = []
    for record in medical_records:
        print(record)
        record_data = {
            "record_id": record.id,
            "date_of_record": record.date_of_record,
            "billing": record.billing,
            "prescriptions": record.prescriptions,
            "advise": record.advise,
            "appointment_id": record.appointment.id,
            "appointment_date": record.appointment.date,
            "time_slot": record.appointment.time_slot,
            "description": record.appointment.description,
            "patient_id": record.appointment.patient.id,
            "patient_first_name": record.appointment.patient.first_name,
            "patient_last_name": record.appointment.patient.last_name,
            "patient_contact": record.appointment.patient.phone,
            "patient_email": record.appointment.patient.email,
        }
        records_with_appointment.append(record_data)
    
    print("Records", records_with_appointment)
    return {"msg":"Record added" , "records" :records_with_appointment }


# def getMedicalRecord(db: Session, patient_id : int):
#     medical_records = (
#         db.query(MedicalRecords)
#         .join(Appointment, Appointment.id == MedicalRecords.appointment_id)
#         .join(Employee, Employee.id == Appointment.doctor_id)
#         .all()
#     )
    
#     records_with_appointment = []
#     for record in medical_records:
#         appointment = db.query(Appointment).filter(Appointment.patient_id == patient_id).first()
#         if appointment:
#             record_data = {
#                 "appointment_id": record.appointment_id,
#                 "date_of_record": record.date_of_record,
#                 "billing": record.billing,
#                 "prescriptions": record.prescriptions,
#                 "advise": record.advise,
#                 "appointment_details": {
#                     "id": appointment.id,
#                     "patient_name":appointment.description,
#                     "doctordetails":{
#                         "doctor" : 
#                     }
#                 }
#             }
#             records_with_appointment.append(record_data)
#     print(records_with_appointment)
#     return {"records": records_with_appointment}
#     # medicalRecords = db.query(MedicalRecords).join(Appointment, Appointment.id == MedicalRecords.appointment_id).all()
#     # print("medical records of the patient", medicalRecords)
#     # return {"records" :medicalRecords }

def getMedicalRecordbyAppointmentID(db: Session, appointment_id: int):
    print("entered")
    medical_records = (
        db.query(MedicalRecords)
        .filter(MedicalRecords.appointment_id == appointment_id)
        .all()
    )
    return medical_records

def getMedicalRecord(db: Session, patient_id: int):
    print("entered")
    medical_records = (
        db.query(MedicalRecords)
        .join(Appointment, Appointment.id == MedicalRecords.appointment_id)
        .join(Employee, Employee.id == Appointment.doctor_id)
        .filter(Appointment.patient_id == patient_id)
        .all()
    )

    records_with_appointment = []
    for record in medical_records:
        print(record)
        record_data = {
            "record_id": record.id,
            "date_of_record": record.date_of_record,
            "billing": record.billing,
            "prescriptions": record.prescriptions,
            "advise": record.advise,
            "appointment_id": record.appointment.id,
            "appointment_date": record.appointment.date,
            "time_slot": record.appointment.time_slot,
            "description": record.appointment.description,
            "doctor_id": record.appointment.doctor.id,
            "doctor_salutation": record.appointment.doctor.salutation,
            "doctor_first_name": record.appointment.doctor.first_name,
            "doctor_last_name": record.appointment.doctor.last_name,
            "doctor_contact": record.appointment.doctor.phone,
            "octor_email": record.appointment.doctor.email,
            "doctor_qualification": record.appointment.doctor.qualification,
            "doctor_department": record.appointment.doctor.department,
        }
        records_with_appointment.append(record_data)
    
    print("Records", records_with_appointment)
    return records_with_appointment


def getMedicalRecordofDoctors(db: Session, doctor_id: int):

    medical_records = (
        db.query(MedicalRecords)
        .join(Appointment, Appointment.id == MedicalRecords.appointment_id)
        .join(Patient, Patient.id == Appointment.patient_id)
        .filter(Appointment.doctor_id == doctor_id)
        .all()
    )

    records_with_appointment = []
    for record in medical_records:
        print(record)
        record_data = {
            "record_id": record.id,
            "date_of_record": record.date_of_record,
            "billing": record.billing,
            "prescriptions": record.prescriptions,
            "advise": record.advise,
            "appointment_id": record.appointment.id,
            "appointment_date": record.appointment.date,
            "time_slot": record.appointment.time_slot,
            "description": record.appointment.description,
            "patient_id": record.appointment.patient.id,
            "patient_first_name": record.appointment.patient.first_name,
            "patient_last_name": record.appointment.patient.last_name,
            "patient_contact": record.appointment.patient.phone,
            "patient_email": record.appointment.patient.email,
        }
        records_with_appointment.append(record_data)
    
    print("Records", records_with_appointment)
    return records_with_appointment