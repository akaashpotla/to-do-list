from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SQLEnum

from app.core.enums import TaskStatus
from app.db.base import Base

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    state: Mapped[TaskStatus] = mapped_column(SQLEnum(TaskStatus), default=TaskStatus.OPEN)

    user = relationship("User", back_populates="tasks")