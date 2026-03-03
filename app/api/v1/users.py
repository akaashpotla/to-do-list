from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db.session import get_db
from app.models.user import User as UserModel
from app.schemas import User as UserSchema, UserResponse
from app.core.hashing import get_password_hash

router = APIRouter(prefix="/api/v1", tags=["users"])


@router.post("/user", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserSchema, db: Session = Depends(get_db)):
    user = UserModel(
        name=payload.name,
        email=str(payload.email),
        password=get_password_hash(payload.password),
    )

    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists",
        )

    db.refresh(user)
    return user
