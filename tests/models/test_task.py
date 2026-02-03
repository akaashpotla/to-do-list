import pytest
from sqlalchemy.exc import IntegrityError
from app.models import Task
from app.models import User

from app.core.enums import TaskStatus

NAME = "Akaash Potla"
EMAIL = "akaash@gmail.com"
PASSWORD = "password"
TITLE = "Reservation Planning"

class TestTask:

    def test_create__success(self, db_session):
        user = User(name=NAME, email=EMAIL, password=PASSWORD)
        db_session.add(user)
        db_session.commit()
        task = Task(user_id=user.id, title=TITLE, state=TaskStatus.DELETED)
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)
        assert task.user_id == user.id
        assert task.title == TITLE
        assert task.id is not None
        assert task.state == TaskStatus.DELETED

    def test_task_title_error(self, db_session):
        user = User(name=NAME, email=EMAIL, password=PASSWORD)
        db_session.add(user)
        db_session.commit()
        task = Task(user_id=user.id, state=TaskStatus.DELETED)
        db_session.add(task)
        with pytest.raises(IntegrityError):
            db_session.commit()

    def test_task_state_default(self, db_session):
        user = User(name=NAME, email=EMAIL, password=PASSWORD)
        db_session.add(user)
        db_session.commit()
        task = Task(user_id=user.id, title=TITLE)
        db_session.add(task)
        db_session.commit()
        assert task.state == TaskStatus.OPEN

    def test_task_user_error(self, db_session):
        task = Task(title=TITLE)
        db_session.add(task)
        with pytest.raises(IntegrityError):
            db_session.commit()