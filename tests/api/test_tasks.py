from app.core.hashing import get_password_hash
from app.models.user import User


URL = "/api/v1/task"
AUTH_URL = "/api/v1/user/auth"
TASK_URL = "/api/v1/task"

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

    def test_create_task_without_auth(self, client, db_session):
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

class TestTaskUpdate:
    
    def test_update_state_success(self, client, db_session):
        create_user(db_session)
        header = get_auth_token(client)

        response = client.post(URL, json={"title": "Do hw"}, headers=header)
        data = response.json()
        task_id = data["id"]
        resp = client.put(f"{TASK_URL}/{task_id}", json={"state": "completed"}, headers=header)
        assert resp.status_code == 200
        assert resp.json()["state"] == "completed"
    
    def test_update_title_success(self, client, db_session):
        create_user(db_session)
        header = get_auth_token(client)

        response = client.post(URL, json={"title": "Do english hw"}, headers=header)
        data = response.json()
        task_id = data["id"]
        resp = client.put(f"{TASK_URL}/{task_id}", json={"title": "Do science hw"}, headers=header)
        assert resp.status_code == 200
        assert resp.json()["title"] == "Do science hw"
        
    def test_update_both_fields_success(self, client, db_session):
        create_user(db_session)
        header = get_auth_token(client)

        response = client.post(URL, json={"title": "Do english hw"}, headers=header)
        data = response.json()
        task_id = data["id"]
        resp = client.put(f"{TASK_URL}/{task_id}", json={"title": "Do science hw", "state": "completed"}, headers=header)
        assert resp.status_code == 200
        assert resp.json()["state"] == "completed"
        assert resp.json()["title"] == "Do science hw"

    def test_update_empty_title(self, client, db_session):
        create_user(db_session)
        header = get_auth_token(client)

        response = client.post(URL, json={"title": "Do hw"}, headers=header)
        data = response.json()
        task_id = data["id"]
        resp = client.put(f"{TASK_URL}/{task_id}", json={"title": ""}, headers=header)
        assert resp.status_code == 422

    def test_update_task_wrong_id(self, client, db_session):
        create_user(db_session)
        header = get_auth_token(client)

        response = client.post(URL, json={"title": "Do english hw"}, headers=header)
        resp = client.put(f"{TASK_URL}/1234", json={"title": "Do science hw"}, headers=header)
        assert resp.status_code == 404
