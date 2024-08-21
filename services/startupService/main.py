from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta, time
from sqlalchemy import engine_from_config, pool
from database.databaseconnection import SQLALCHEMY_DATABASE_URL,Base
from database.models import Employee, AppointmentSlots

def generate_and_store_slots(engine):
    Session = sessionmaker(bind=engine)
    session = Session()

    doctors = session.query(Employee).filter(Employee.role.in_(["Doctor", "doctor"])).all()  # Retrieve all doctors from the database
    for doctor in doctors:
        current_time = doctor.shift_start
        slots = []

        while True:

            current_time_dt = datetime.combine(datetime.today(), current_time)  # Temporarily combine with any date to perform arithmetic
            slot_end_time_dt = current_time_dt + timedelta(minutes=15)
            slot_end_time = slot_end_time_dt.time()

            if doctor.shift_end == time(0, 0):  # If shift ends at midnight, adjust comparison
                if current_time >= time(23, 45):
                    break
            elif slot_end_time > doctor.shift_end:
                break
            
            existing_slot = session.query(AppointmentSlots).filter(AppointmentSlots.doctor_id==doctor.id,
                                                                   AppointmentSlots.slot_start==current_time,
                                                                   AppointmentSlots.slot_end==slot_end_time).first()
            if existing_slot is None:
                slots.append(AppointmentSlots(
                    doctor_id=doctor.id,
                    slot_start=current_time,
                    slot_end=slot_end_time
                ))
            else:
                pass
            current_time = slot_end_time

        session.add_all(slots)
        session.commit()
        print(f"Added {len(slots)} time-only slots to the database for Doctor ID: {doctor.id}.")

    session.close()

def check_and_initialize_tables():
    engine = engine_from_config(
        configuration={"sqlalchemy.url": SQLALCHEMY_DATABASE_URL},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    Base.metadata.create_all(engine)
    print("Database tables checked and initialized.")
    
    generate_and_store_slots(engine)


if __name__ == "__main__":
    check_and_initialize_tables()