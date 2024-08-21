from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

#SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:netweb12@localhost/HospitalManagementSystem"
# NOTE Uncomment before line and comment above line while using in docker
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()