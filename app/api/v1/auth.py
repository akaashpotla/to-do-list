from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import models
import app.core.hashing as hashing
from app.core import token
from app.db import session
router = APIRouter(prefix="/api/v1/user", tags=['Authentication'])

@router.post('/auth')
def login(response: Response, request:OAuth2PasswordRequestForm = Depends(), db:Session = Depends(session.get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid Credentials",
            headers = {"WWW-Authenticate": "Bearer"}
        )
    if not hashing.verify_password(request.password, user.password):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Incorrect Credentials",
            headers = {"WWW-Authenticate": "Bearer"}
        )
    access_token = token.create_access_token(data = {"sub": user.email})
    response.set_cookie(key="access_token", value=access_token, httponly=True, samesite='lax')
    return {"message": "Login successful!"}

@router.post('/logout')
def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        httponly=True,
        samesite='lax'
    )
    return {"message": "Logged out."}