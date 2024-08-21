from fastapi import FastAPI
from app.api import authentication_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(authentication_router.router,prefix="/authentication")

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials=True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)