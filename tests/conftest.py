import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.db.session import get_db
from app.main import app
from app.core.config import settings
from app.db.base import Base

@pytest.fixture()
def db_session():
    engine = create_engine(settings.DATABASE_URL)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    connection = engine.connect()
    
    LocalTestingSession = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=connection
    )
    
    db = LocalTestingSession()

    try:
        yield db
    finally:
        db.rollback()
        db.close()
        connection.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()