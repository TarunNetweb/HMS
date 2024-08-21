from sqlalchemy import Column, Integer, String, Date, Boolean, Float, ForeignKey
from sqlalchemy.types import Time
from sqlalchemy.orm import relationship
from .databaseconnection import Base
import bcrypt

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(30), nullable=False )
    last_name = Column(String(30), nullable = False)
    date_of_birth = Column(Date, nullable = False)
    age = Column(Integer, nullable = False)
    email = Column(String(255),nullable= False)
    phone = Column(String(10), nullable = False)
    emergency_contact = Column(String(10), nullable = False)
    password_hash = Column(String(255), nullable=False)
    tnc = Column(Boolean, nullable = False)
    height = Column(Float,nullable = True)
    weight = Column(Float,nullable = True)
    blood_type = Column(String(4),nullable = True)
    email_confirmed = Column(Boolean,nullable = True)
    gender = Column(String(6),nullable = False)
    address = Column(String(255),nullable = False)
    city = Column(String(50), nullable = False)
    state = Column(String(50),nullable = False)
    pincode = Column(String(6),nullable = False)
    appointments = relationship("Appointment",back_populates="patient")

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
class Appointment(Base):
    __tablename__ = "appointments"
    
    id = Column(Integer, primary_key = True, index=True)
    date = Column(Date, nullable=False)
    time_slot = Column(String(255), nullable = False)
    description = Column(String(255), nullable = False)
    status = Column(String(10), nullable = False)
    patient_id = Column(Integer,ForeignKey('patients.id'))
    patient = relationship("Patient",back_populates="appointments")
    doctor_id = Column(Integer,ForeignKey('employees.id'))
    doctor = relationship("Employee",back_populates="appointments")
    medicalrecords = relationship("MedicalRecords",back_populates="appointment")
    appointmentidreport = relationship("LabReports",back_populates="appointment")

class AppointmentSlots(Base):
    __tablename__ = "appointmentslots"
    
    id = Column(Integer,primary_key=True, index=True)
    slot_start = Column(Time)
    slot_end = Column(Time)
    doctor_id = Column(Integer,ForeignKey("employees.id"))
    doctor=relationship("Employee",back_populates="appointment_slots")
    
class Employee(Base):
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key = True, index = True)
    salutation = Column(String(4), nullable = False)
    first_name = Column(String(20),nullable = False)
    last_name = Column(String(20),nullable = False)
    date_of_birth = Column(Date,nullable = False)
    age = Column(Integer,nullable = False)
    phone = Column(String(10), nullable = False)
    email = Column(String(255),nullable = False)
    emergency_contact = Column(String(10), nullable = False)
    password_hash = Column(String(255), nullable=False)
    gender = Column(String(6),nullable = False)
    address = Column(String(255),nullable = False)
    city = Column(String(50), nullable = False)
    state = Column(String(50),nullable = False)
    pincode = Column(String(6),nullable = False)
    role = Column(String(20),nullable = False)
    qualification = Column(String(1000),nullable = False)
    department = Column(String(20),nullable = False)
    bio = Column(String(1000),nullable = True)
    shift_start = Column(Time,nullable = True)
    shift_end = Column(Time,nullable = True)
    appointment_slots = relationship("AppointmentSlots",back_populates="doctor")
    appointments = relationship("Appointment",back_populates="doctor")
    
    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

class Inventory(Base):
    __tablename__ = "inventory"
   
    id = Column(Integer,primary_key=True, index=True)
    name_of_equipment =  Column(String(255), nullable = False)
    category_of_equipment =  Column(String(255), nullable = False)
    stock_of_equipment =  Column(Integer, nullable = False)
    unit_price = Column(Integer, nullable = False)
    total_value = Column(Integer, nullable = False)
    date_of_purchase = Column(Date, nullable = False)

    def setTotalPrice(self):
        self.total_value = self.unit_price * self.stock_of_equipment


class MedicalRecords(Base):
    __tablename__ = "medicalrecords"
    id = Column(Integer,primary_key=True, index=True)
    prescriptions  =  Column(String(255), nullable = False)
    advise =  Column(String(255), nullable = False)
    billing = Column(Integer, nullable = False)
    date_of_record = Column(Date, nullable = False)
    appointment_id = Column(Integer,ForeignKey('appointments.id'))
    appointment = relationship("Appointment",back_populates="medicalrecords")


class LabReports(Base):
    __tablename__ = "medicalreports"
    id = Column(Integer,primary_key=True, index=True)
    chief_complaint = Column(String(255), nullable=False)
    history_of_present_illness = Column(String(255), nullable=False)
    past_medical_history = Column(String(255), nullable=False)
    medication_history = Column(String(255), nullable=False)
    family_history = Column(String(255), nullable=False)
    social_history = Column(String(255), nullable=False)
    review_of_systems = Column(String(255), nullable=False)
    physical_exam_findings = Column(String(255), nullable=False)
    appointment_id = Column(Integer,ForeignKey('appointments.id'))
    appointment = relationship("Appointment",back_populates="appointmentidreport")
    blood_report_id = Column(Integer,ForeignKey('bloodreport.id'))
    blood_report = relationship("BloodReport",back_populates="bloodreportid")

class BloodReport(Base):
    __tablename__ = "bloodreport"
    id = Column(Integer,primary_key=True, index=True)
    wbc_count = Column(Float)
    rbc_count = Column(Float)
    hemoglobin = Column(Float)
    hematocrit = Column(Float)
    mean_corpuscular_volume = Column(Float)
    mean_corpuscular_hemoglobin = Column(Float)
    mean_corpuscular_hemoglobin_concentration = Column(Float)
    platelet_count = Column(Float)
    
    neutrophils = Column(Float)
    lymphocytes = Column(Float)
    monocytes = Column(Float)
    eosinophils = Column(Float)
    basophils = Column(Float)
    
    glucose = Column(Float)
    sodium = Column(Float)
    potassium = Column(Float)
    chloride = Column(Float)
    bicarbonate = Column(Float)
    alt = Column(Float)
    ast = Column(Float)
    alp = Column(Float)
    bilirubin = Column(Float)
    creatinine = Column(Float)
    bun = Column(Float)
    total_cholesterol = Column(Float)
    good_cholesterol = Column(Float)
    bad_cholesterol = Column(Float)
    triglycerides = Column(Float)
    prothrombin_time = Column(Float)
    international_normalized_ratio = Column(Float)
    partial_thrombin_time = Column(Float)

    blood_group = Column(String(10))
    rh_factor = Column(String(10))
    crp = Column(Float)
    esr = Column(Float)
    ferritin = Column(Float)
    bloodreportid =  relationship("LabReports",back_populates="blood_report")