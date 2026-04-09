from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session

from app.db.session import get_db
from . import token
from app.models.user import User as UserModel

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/user/auth")

def get_current_user(request: Request, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    token_data = request.cookies.get("access_token")
    if not token_data:
        raise credentials_exception
    
    email = token.verify_token(token_data, credentials_exception)
    
    user = db.query(UserModel).filter(UserModel.email == email).first()
    if user is None:
        raise credentials_exception
    return user
