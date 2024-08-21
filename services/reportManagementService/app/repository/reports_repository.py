from sqlalchemy.orm import Session
from database.models import LabReports, BloodReport, Appointment, Patient
from app.schemas.models import MedicalReportBase, TypeOfMedicalReport
from datetime import datetime
import pytz
from fastapi import HTTPException, status

def get_medical_report(db: Session, medical_report_id :  int):
    medical_report_existing = db.query(LabReports).filter(LabReports.appointment_id == medical_report_id).first()
    return medical_report_existing

def get_specific_report_of_patient(db: Session, report_id :  int, type_of_report:TypeOfMedicalReport):
    print("ddfjd ---> ", report_id, type_of_report)
    if type_of_report.required_report == "Blood Report":
        medical_report = (
            db.query(LabReports)
            .join(BloodReport, BloodReport.id == LabReports.blood_report_id)
            .all()
            )
        print("fdfglf", medical_report)
        print("fdfglfdffs", len(medical_report))
        medical_report_of_one_patient = []
        for i in medical_report:
            if i.blood_report.id == report_id:
                medical_report_of_one_patient.append(i)
                return i.blood_report



def get_all_reports(db: Session):
    medical_records = (
        db.query(LabReports)
        .join(Appointment, Appointment.id == LabReports.appointment_id)
        .join(Patient, Patient.id == Appointment.patient_id)
        .all()
    )
    medical_reports_of_all_patients = []
    for i in medical_records:
            if i.blood_report and i.appointment and i.appointment.patient and i.appointment.doctor:
                medical_reports_of_all_patients.append(i)
    return medical_reports_of_all_patients

def get_all_reports_of_patient(db: Session, patient :  int):
    medical_records = (
        db.query(LabReports)
        .join(Appointment, Appointment.id == LabReports.appointment_id)
        .join(Patient, Patient.id == Appointment.patient_id)
        .all()
    )
    medical_reports_of_one_patient = []
    for i in medical_records:
        if i.appointment.patient.id == patient:
            medical_reports_of_one_patient.append(i)
    return medical_reports_of_one_patient

def create_new_medical_report(db: Session, new_medical_report :  MedicalReportBase):
    LabReports_New = LabReports(
    chief_complaint = new_medical_report.chief_complaint,
    history_of_present_illness = new_medical_report.history_of_present_illness ,
    past_medical_history = new_medical_report.past_medical_history ,
    medication_history = new_medical_report.medication_history ,
    family_history = new_medical_report.family_history ,
    social_history = new_medical_report.social_history ,
    review_of_systems = new_medical_report.review_of_systems ,
    physical_exam_findings = new_medical_report.physical_exam_findings ,
    )

    if new_medical_report.appointment_id:
        LabReports_New.appointment_id = new_medical_report.appointment_id
    if new_medical_report.review_of_systems == "Blood Report":    
        Blood_Report_New = BloodReport()
        if new_medical_report.wbc_count:
            Blood_Report_New.wbc_count = new_medical_report.wbc_count
        if new_medical_report.chloride:
            Blood_Report_New.chloride = new_medical_report.chloride
        if new_medical_report.bad_cholesterol:
            Blood_Report_New.bad_cholesterol = new_medical_report.bad_cholesterol
        if new_medical_report.alp:
            Blood_Report_New.alp = new_medical_report.alp
        if new_medical_report.bilirubin:
            Blood_Report_New.bilirubin = new_medical_report.bilirubin
        if new_medical_report.good_cholesterol:
            Blood_Report_New.good_cholesterol = new_medical_report.good_cholesterol
        if new_medical_report.hematocrit:
            Blood_Report_New.hematocrit = new_medical_report.hematocrit
        if new_medical_report.ast:
            Blood_Report_New.ast = new_medical_report.ast
        if new_medical_report.rbc_count:
            Blood_Report_New.rbc_count = new_medical_report.rbc_count
        if new_medical_report.alt:
            Blood_Report_New.alt = new_medical_report.alt
        if new_medical_report.total_cholesterol:
            Blood_Report_New.total_cholesterol = new_medical_report.total_cholesterol
        if new_medical_report.bicarbonate:
            Blood_Report_New.bicarbonate = new_medical_report.bicarbonate
        if new_medical_report.hemoglobin:
            Blood_Report_New.hemoglobin = new_medical_report.hemoglobin
        if new_medical_report.mean_corpuscular_hemoglobin:
            Blood_Report_New.mean_corpuscular_hemoglobin = new_medical_report.mean_corpuscular_hemoglobin
        if new_medical_report.mean_corpuscular_hemoglobin_concentration:
            Blood_Report_New.mean_corpuscular_hemoglobin_concentration = new_medical_report.mean_corpuscular_hemoglobin_concentration
        if new_medical_report.mean_corpuscular_volume:
            Blood_Report_New.mean_corpuscular_volume = new_medical_report.mean_corpuscular_volume
        if new_medical_report.basophils:
            Blood_Report_New.basophils = new_medical_report.basophils
        if new_medical_report.eosinophils:
            Blood_Report_New.eosinophils = new_medical_report.eosinophils
        if new_medical_report.glucose:
            Blood_Report_New.glucose = new_medical_report.glucose
        if new_medical_report.sodium:
            Blood_Report_New.sodium = new_medical_report.sodium
        if new_medical_report.platelet_count:
            Blood_Report_New.platelet_count = new_medical_report.platelet_count
        if new_medical_report.lymphocytes:
            Blood_Report_New.lymphocytes = new_medical_report.lymphocytes
        if new_medical_report.neutrophils:
            Blood_Report_New.neutrophils = new_medical_report.neutrophils
        if new_medical_report.monocytes:
            Blood_Report_New.monocytes = new_medical_report.monocytes
        if new_medical_report.potassium:
            Blood_Report_New.potassium = new_medical_report.potassium
        if new_medical_report.creatinine:
            Blood_Report_New.creatinine = new_medical_report.creatinine
        if new_medical_report.bun:
            Blood_Report_New.bun = new_medical_report.bun
        if new_medical_report.triglycerides:
            Blood_Report_New.triglycerides = new_medical_report.triglycerides  
        if new_medical_report.prothrombin_time:
            Blood_Report_New.prothrombin_time = new_medical_report.prothrombin_time
        if new_medical_report.international_normalized_ratio:
            Blood_Report_New.international_normalized_ratio = new_medical_report.international_normalized_ratio
        if new_medical_report.partial_thrombin_time:
            Blood_Report_New.partial_thrombin_time = new_medical_report.partial_thrombin_time
        db.add(Blood_Report_New)
        db.commit()
        db.refresh(Blood_Report_New)
        LabReports_New.blood_report_id = Blood_Report_New.id


    db.add(LabReports_New)
    db.commit()
    db.refresh(LabReports_New)
    
    db.add(Blood_Report_New)
    db.commit()
    db.refresh(Blood_Report_New)
    return {"msg":"Report Addition Successful"}



def update_medical_report(db: Session, report_id: int,udpated_medical_report :  MedicalReportBase):
    medical_report = db.query(LabReports).filter(LabReports.id == report_id).first()
   
    medical_report.chief_complaint = udpated_medical_report.first_name
    medical_report.history_of_present_illness = udpated_medical_report.last_name
    medical_report.past_medical_history = udpated_medical_report.date_of_birth
    medical_report.medication_history = udpated_medical_report.email
    medical_report.family_history = udpated_medical_report.phone
    medical_report.social_history = udpated_medical_report.emergency_contact
    medical_report.review_of_systems = udpated_medical_report.height
    medical_report.physical_exam_findings = udpated_medical_report.gender

    db.commit()
    db.refresh(medical_report)
    return medical_report
