from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.base import Base
from app.db.session import engine

from contextlib import asynccontextmanager
from app.db.session import get_db
from app.api.v1.users import router as users_router
from app.api.v1.auth import router as auth_router
from app.api.v1.tasks import router as tasks_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="To-Do List API",
    lifespan=lifespan
)

app.include_router(users_router)
app.include_router(auth_router)
app.include_router(tasks_router)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/db-check")
def db_check(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT 1")).scalar_one()
    return {"db": "ok", "result": result}
