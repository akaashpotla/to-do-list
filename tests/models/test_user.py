import pytest
from sqlalchemy.exc import IntegrityError
from app.models import User

NAME = "Akaash Potla"
EMAIL = "akaash@gmail.com"
PASSWORD = "password"

class TestUser:

    def test_create_user_success(self, db_session):
        user = User(
            name = NAME,
            email = EMAIL,
            password = PASSWORD
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        assert user.name == NAME
        assert user.email == EMAIL
        assert user.password == PASSWORD
        assert user.id is not None

    def test_user_name_error(self, db_session):
        user = User(
            email = EMAIL,
            password = PASSWORD
        )
        db_session.add(user)
        with pytest.raises(IntegrityError):
            db_session.commit()

    def test_user_email_error(self, db_session):
        user = User(
            name = NAME,
            password = PASSWORD
        )
        db_session.add(user)
        with pytest.raises(IntegrityError):
            db_session.commit()
            
    def test_user_password_error(self, db_session):
        user = User(
            name = NAME,
            email = EMAIL,
    )
        db_session.add(user)
        with pytest.raises(IntegrityError):
            db_session.commit()
