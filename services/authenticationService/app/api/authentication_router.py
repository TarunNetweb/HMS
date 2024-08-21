from fastapi import APIRouter, HTTPException, status, Depends, Request, Header
from app.schemas.models import AuthenticateUser, UserCreds
from app.utils.auth import authenticate_user
from app.utils.tokenUtils import create_access_token,get_current_user
from database.databaseconnection import SessionLocal
from sqlalchemy.orm import Session
import json 

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# NOTE Check for the validity of the token of a Patient
@router.post("/validateTokenPatient")
async def ValidateToken(Authorization: str = Header(None), db: Session = Depends(get_db)):
    if not Authorization:
        return False
    token = Authorization.split(" ")[1] if Authorization.startswith("Bearer ") else None
    is_valid = await get_current_user(token=token, db=db,type="Patient")
    if not is_valid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    print(is_valid)
    return is_valid

# NOTE Check for the validity of the token of Staff
@router.post("/validateTokenStaff")
async def ValidateTokenStaff(Authorization: str = Header(None), db: Session = Depends(get_db)):
    if not Authorization:
        return False
    token = Authorization.split(" ")[1] if Authorization.startswith("Bearer ") else None
    is_valid = await get_current_user(token=token, db=db,type="Employee")
    if not is_valid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    print(is_valid)
    return is_valid

@router.post("/validateTokenAdmin")
async def ValidateTokenStaff(Authorization: str = Header(None), db: Session = Depends(get_db)):
    if not Authorization:
        return False
    token = Authorization.split(" ")[1] if Authorization.startswith("Bearer ") else None
    is_valid = await get_current_user(token=token, db=db,type="Admin")
    if not is_valid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    print(is_valid)
    return is_valid

# NOTE Login for all the users will be done from here
@router.post("/login")
async def Login(user_creds: UserCreds,db: Session = Depends(get_db)):
    user_role = authenticate_user(creds=user_creds,db=db)
        
    access_token = create_access_token(data={"username":user_creds.username,"role":user_role})
    
    return {"token" : access_token, "role":user_role}