import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool, text
from sqlalchemy.orm import sessionmaker

from ..database import Base
from ..main import app
from ..models import Todos, Users
from ..routers.auth import bcrypt_context, get_current_user

SQLALCHEMY_DATABASE_URI = "sqlite:///./testdb.db"

engine = create_engine(SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False}, poolclass=StaticPool)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {'username': 'shelbytest', 'id': 1, 'user_role': 'admin'}


client = TestClient(app)


@pytest.fixture
def test_todos():
    todos = Todos(
        title="Learn to code!",
        description="Need to learn everyday!",
        priority=5,
        completed=False,
        owner_id=1
    )

    db = TestingSessionLocal()
    db.add(todos)
    db.commit()
    yield todos
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM todos;"))
        conn.commit()

@pytest.fixture
def test_users():
    users = Users(
        username="shelbytest",
        email="shelbytest@email.com",
        first_name="Shelby",
        last_name="Test",
        hashed_password=bcrypt_context.hash("testpassword"),
        role="admin",
        phone_number="+1 555 555 555"
    )
    db = TestingSessionLocal()
    db.add(users)
    db.commit()
    yield users
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM users;"))
        conn.commit()


