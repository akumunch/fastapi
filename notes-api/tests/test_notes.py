import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database import Base, get_db

SQLALCHEMY_TEST_DB_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_TEST_DB_URL,
    connect_args={"check_same_thread": False}  # needed for SQLite
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

# ── Tests ───────────────────────────────────────────────────────────────────
def test_create_note():
    response = client.post("/notes/", json={"title":"Test Note", "content":"Test Content"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Note"
    assert data["content"] == "Test Content"
    assert "id" in data

def test_get_all_notes():
    response = client.get("/notes/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_one_note():
    create = client.post("/notes/",json={"title":"Single Note", "content":"One Line"})
    create_id = create.json()["id"]

    response = client.get(f"/notes/{create_id}")
    data = response.json()
    assert response.status_code == 200
    assert data["title"] == "Single Note" 
    assert data["content"] == "One Line"

def test_update_note():
    create = client.post("/notes/", json={"title": "Old Title", "content": "Old Content"})
    note_id = create.json()["id"]

    response = client.put(f"/notes/{note_id}", json={"title": "New Title"})
    assert response.status_code == 200
    assert response.json()["title"] == "New Title"
    assert response.json()["content"] == "Old Content"

def test_delete_note():
    create = client.post("/notes/", json={"title": "To Delete", "content": "Bye"})
    note_id = create.json()["id"]

    response = client.delete(f"/notes/{note_id}")
    assert response.status_code == 200
    assert response.json()["Message"] == "Deleted Note Successfully"

def test_get_deleted_note_returns_404():
    create = client.post("/notes/", json={"title": "Gone", "content": "Soon"})
    note_id = create.json()["id"]
    client.delete(f"/notes/{note_id}")

    response = client.get(f"/notes/{note_id}")
    assert response.status_code == 404