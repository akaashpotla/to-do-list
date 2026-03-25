from app.core.enums import TaskStatus
from app.core.hashing import get_password_hash
from app.models.user import User
from app.models.task import Task

AUTH_URL = "/api/v1/user/auth"

NAME = "Akaash Potla"
EMAIL = "akaash@gmail.com"
PASSWORD = "1Password!"

def create_user(db_session):
    user = User(
        name=NAME,
        email=EMAIL,
        password=get_password_hash(PASSWORD)
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

def get_auth_token(client):
    response = client.post(AUTH_URL, data={"username": EMAIL, "password": PASSWORD})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def create_task(db_session, user, title="Do hw"):
    task = Task(
        title=title,
        user_id=user.id,
        state=TaskStatus.OPEN
    )
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)
    return task