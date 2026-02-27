from app.core.hashing import get_password_hash
from app.models.user import User


URL = "/api/v1/task"
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

class TestTaskCreation:
    
    def test_create_task_success(self, client, db_session):
        created_user = create_user(db_session)
        header = get_auth_token(client)
        payload = {
            "title": "Do hw"
        }
        response = client.post(URL, json=payload, headers=header)
        assert response.status_code == 201
        data = response.json()

        assert "id" in data
        assert data["title"] == payload["title"]
        assert data["user_id"] == created_user.id
        assert "state" in data
        
    def test_empty_payload(self, client, db_session):
        create_user(db_session)
        header = get_auth_token(client)
        payload = {
        }
        response = client.post(URL, json=payload, headers=header)
        assert response.status_code == 422

    def test_title_empty_string(self, client, db_session):
        create_user(db_session)
        header = get_auth_token(client)
        payload = {
            "title" : ""
        }
        response = client.post(URL, json=payload, headers=header)
        assert response.status_code==422

    def test_create_task_failure(self, client, db_session):
        create_user(db_session)
        header = get_auth_token(client)
        payload = {
            "title" : "Do hw"
        }
        response = client.post(URL, json=payload)
        assert response.status_code==401

    def test_create_task_invalid_token(self, client, db_session):
        create_user(db_session)
        header = get_auth_token(client)
        payload = {
            "title" : "Do hw"
        }
        response = client.post(URL, json=payload, headers={"Authorization": f"Bearer invalid token"})
        assert response.status_code==401