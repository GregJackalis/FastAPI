from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..import database, schemas, tables, utils, oauth2
router = APIRouter(tags=["Authentication"],
                   prefix="/login")


@router.post("/", response_model= schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db : Session = Depends(database.get_db)):

    user = db.query(tables.Users).filter(tables.Users.email == user_credentials.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    if not utils.verifying_hashed_passwords(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Invalid Credentials")
    

    #create token
    access_token = oauth2.create_access_token(data= {"user_id": user.id})
    #return token
    return {"access_token": access_token, "token_type": "bearer"}

