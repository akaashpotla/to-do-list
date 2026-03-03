from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.oauth2 import get_current_user
from app.db.session import get_db
from app.models.task import Task as TaskModel
from app.schemas import Task as TaskSchema, TaskResponse

router = APIRouter(prefix="/api/v1", tags=["tasks"])


@router.post("/task", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskSchema, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    task = TaskModel(
        title=payload.title,
        user_id=current_user.id
    )

    db.add(task)
    db.commit()
    db.refresh(task)
    return task
