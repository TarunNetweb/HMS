from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .auth import authorized_employee,authorized_patient,authorized_admin
from sqlalchemy.orm import Session

ACCESS_TOKEN_EXPIRE_HOURS = 24
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = 'Th1515s3cR3tK#Y'              # TODO Remember to use this in form of ENVIRONMENT VARIABLE

# NOTE Function to create a new access token with expiry of 24 hours
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode.update({'exp':expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt
 
# NOTE Function to get the current user in order to validate
async def get_current_user(db:Session,type: str,token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        details: dict = {
            'username': payload.get("username"),
            'role': payload.get('role')
        }
        
        if type=="Patient":
            userFromDb = authorized_patient(db = db, username=details["username"], role=details["role"])
        elif type=="Employee":
            userFromDb = authorized_employee(db = db, username=details["username"])
        elif type=="Admin":
            userFromDb = authorized_admin(db=db,username=details["username"])

        if userFromDb is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return details
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )