import uuid
from app.models import User
from app.db.session import SessionLocal


class TestUser:
    def test_create_user(self):
        db = SessionLocal()
        unique_email = f"akaash+{uuid.uuid4()}@gmail.com"
        user = User(name="Akaash Potla", email=unique_email, password="password")
        db.add(user)
        db.commit()
        assert user.name == "Akaash Potla"
        assert user.email == unique_email
        assert user.password == "password"
        assert user.id is not None
