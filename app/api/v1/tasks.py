from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.oauth2 import get_current_user
from app.db.session import get_db
from app.models.task import Task as TaskModel
from app.schemas import Task as TaskSchema, TaskResponse, TaskUpdate

router = APIRouter(prefix="/api/v1", tags=["tasks"])


@router.post("/task", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskSchema, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    task = TaskModel(title=payload.title, user_id=current_user.id
    )

    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@router.put("/task/{id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def update_task(id: int, payload: TaskUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    task = (db.query(TaskModel).filter(TaskModel.id==id, TaskModel.user_id==current_user.id).first())

    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    
    if payload.title is not None:
        task.title = payload.title
    if payload.state is not None:
        task.state = payload.state

    db.commit()
    db.refresh(task)
    return task
