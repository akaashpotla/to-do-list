import jwt

from app.models.user import User
from app.core.hashing import get_password_hash
from app.core.config import settings

URL = "/api/v1/user/auth"

NAME = "Akaash Potla"
EMAIL = "akaash@gmail.com"
PASSWORD = "1Password!"

def create_user(db_session):
        user=User(
            name=NAME,
            email=EMAIL,
            password=get_password_hash(PASSWORD)
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        return user

class TestAuthValid:
    
    def test_missing_username(self, client):
        response = client.post(URL, data = {"password" : PASSWORD})
        assert response.status_code == 422
        
    def test_missing_password(self, client):
        response = client.post(URL, data = {"username" : EMAIL})
        assert response.status_code == 422

    def test_invalid_user(self, client):
        response = client.post(URL, data = {"username" : "missingemail@gmail.com", "password" : PASSWORD})
        assert response.status_code == 401

    def test_wrong_password(self, client, db_session):
        create_user(db_session)
        response = client.post(URL, data = {"username" : EMAIL, "password" : "1Wrongpassword!"})
        assert response.status_code == 401

    def test_login_success(self, client, db_session):
        create_user(db_session)
        response = client.post(URL, data = {"username" : EMAIL, "password" : PASSWORD})
        assert response.status_code == 200

