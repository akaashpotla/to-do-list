from tests.helper import create_user, create_task, get_auth_token, NAME, EMAIL, PASSWORD

AUTH_URL = "/api/v1/user/auth"
TASK_URL = "/api/v1/task"

class TestTaskCreation:
    
    def test_create_task_success(self, client, db_session):
        created_user = create_user(db_session)
        header = get_auth_token(client)
        payload = {"title": "Do hw"}
        response = client.post(TASK_URL, json=payload, headers=header)
        assert response.status_code == 201
        data = response.json()

        assert "id" in data
        assert data["title"] == payload["title"]
        assert data["user_id"] == created_user.id
        assert "state" in data
        
    def test_empty_payload(self, client, db_session):
        create_user(db_session)
        header = get_auth_token(client)
        payload = {}
        response = client.post(TASK_URL, json=payload, headers=header)
        assert response.status_code == 422

    def test_title_empty_string(self, client, db_session):
        create_user(db_session)
        header = get_auth_token(client)
        payload = {"title" : ""}
        response = client.post(TASK_URL, json=payload, headers=header)
        assert response.status_code==422

    def test_create_task_without_auth(self, client, db_session):
        create_user(db_session)
        header = get_auth_token(client)
        payload = {"title" : "Do hw"}
        response = client.post(TASK_URL, json=payload)
        assert response.status_code==401

    def test_create_task_invalid_token(self, client, db_session):
        create_user(db_session)
        header = get_auth_token(client)
        payload = {"title" : "Do hw"}
        response = client.post(TASK_URL, json=payload, headers={"Authorization": f"Bearer invalid token"})
        assert response.status_code==401

class TestTaskUpdate:
    
    def test_update_state_success(self, client, db_session):
        user= create_user(db_session)
        header = get_auth_token(client)

        task = create_task(db_session, user)
        resp = client.put(f"{TASK_URL}/{task.id}", json={"state": "completed"}, headers=header)
        assert resp.status_code == 200
        assert resp.json()["state"] == "completed"
    
    def test_update_title_success(self, client, db_session):
        user = create_user(db_session)
        header = get_auth_token(client)

        task = create_task(db_session, user, title="Do english hw")
        resp = client.put(f"{TASK_URL}/{task.id}", json={"title": "Do science hw"}, headers=header)
        assert resp.status_code == 200
        assert resp.json()["title"] == "Do science hw"
        
    def test_update_both_fields_success(self, client, db_session):
        user = create_user(db_session)
        header = get_auth_token(client)

        task = create_task(db_session, user, title="Do english hw")
        resp = client.put(f"{TASK_URL}/{task.id}", json={"title": "Do science hw", "state": "completed"}, headers=header)
        assert resp.status_code == 200
        assert resp.json()["state"] == "completed"
        assert resp.json()["title"] == "Do science hw"

    def test_update_empty_title(self, client, db_session):
        user = create_user(db_session)
        header = get_auth_token(client)

        task = create_task(db_session, user)
        resp = client.put(f"{TASK_URL}/{task.id}", json={"title": ""}, headers=header)
        assert resp.status_code == 422

    def test_update_task_wrong_id(self, client, db_session):
        user = create_user(db_session)
        header = get_auth_token(client)

        create_task(db_session, user, title="Do english hw")
        resp = client.put(f"{TASK_URL}/1234", json={"title": "Do science hw"}, headers=header)
        assert resp.status_code == 404

class TestTaskDelete:
    def test_delete_task_successful(self, client, db_session):
        user = create_user(db_session)
        header = get_auth_token(client)

        task = create_task(db_session, user)
        resp = client.delete(f"{TASK_URL}/{task.id}", headers=header)
        assert resp.status_code == 204

    def test_delete_task_wrong_id(self, client, db_session):
        create_user(db_session)
        header = get_auth_token(client)
        resp = client.delete(f"{TASK_URL}/999999", headers=header)
        assert resp.status_code == 404

    def test_delete_task_unauthorized(self, client, db_session):
        user = create_user(db_session)
        get_auth_token(client)

        task = create_task(db_session, user)
        resp = client.delete(f"{TASK_URL}/{task.id}")
        assert resp.status_code == 401

class TestGetOpenTasks:
    def test_get_open_tasks_successful(self, client, db_session):
        user = create_user(db_session)
        header = get_auth_token(client)
        create_task(db_session, user, title="Task 1")
        create_task(db_session, user, title="Task 2")
        resp = client.get(TASK_URL, headers=header)
        assert resp.status_code == 200
        assert len(resp.json()["tasks"]) == 2

    def test_get_zero_open_tasks(self, client, db_session):
        create_user(db_session)
        header = get_auth_token(client)
        resp = client.get(TASK_URL, headers=header)
        assert resp.status_code == 200
        assert len(resp.json()["tasks"]) == 0

    def test_get_open_tasks_without_completed(self, client, db_session):
        user = create_user(db_session)
        header = get_auth_token(client)
        task = create_task(db_session, user, title="Task 1")
        client.put(f"{TASK_URL}/{task.id}", json={"state": "completed"}, headers=header)
        resp = client.get(TASK_URL, headers=header)
        assert resp.status_code == 200
        assert len(resp.json()["tasks"]) == 0
    
class TestGetCompletedTasks:
    def test_get_completed_tasks_successful(self, client, db_session):
        user = create_user(db_session)
        header = get_auth_token(client)
        task = create_task(db_session, user, title="Task 1")
        client.put(f"{TASK_URL}/{task.id}", json={"state": "completed"}, headers=header)
        resp = client.get(f"{TASK_URL}/completed", headers=header)
        assert resp.status_code == 200
        assert len(resp.json()["tasks"]) == 1

    def test_get_zero_completed_tasks(self, client, db_session):
        user = create_user(db_session)
        header = get_auth_token(client)
        create_task(db_session, user, title="Task 1")
        resp = client.get(f"{TASK_URL}/completed", headers=header)
        assert resp.status_code == 200
        assert len(resp.json()["tasks"]) == 0
