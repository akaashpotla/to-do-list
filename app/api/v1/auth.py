from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import models
import app.core.hashing as hashing
from app.core import token
from app.db import session
router = APIRouter(
    tags=['Authentication']
)

@router.post('/auth')
def login(request:OAuth2PasswordRequestForm = Depends(),db:Session = Depends(session.get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Credentials")
    if not hashing.verify_password(user.password,request.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incorrect password")
    access_token = token.create_access_token(data={"sub": user.email})
    return {"access_token": access_token,"token_type": "bearer"}

