from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import employee_router, doctor_router

app = FastAPI()

app.include_router(employee_router.router,prefix="/employee")
app.include_router(doctor_router.router,prefix="/doctor")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)