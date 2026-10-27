import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool


@pytest.fixture
def client():
    from database import Base
    from main import app, get_db

    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    session_factory = sessionmaker(bind=engine)

    def override_db():
        with session_factory() as db:
            yield db

    app.dependency_overrides[get_db] = override_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


def author(client, name):
    return client.post("/authors/", json={"name": name, "bio": "Bio"})


def book(client, author_id, title):
    return client.post(f"/authors/{author_id}/books/", json={
        "title": title, "summary": "Summary", "publication_date": "2020-01-02"
    })


def test_create_get_and_duplicate_author(client):
    response = author(client, "Ada")
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Ada" and data["bio"] == "Bio"
    assert client.get(f"/authors/{data['id']}").json()["name"] == "Ada"
    assert author(client, "Ada").status_code == 400
    assert client.get("/authors/999").status_code == 404


def test_author_pagination(client):
    for name in ("A", "B", "C"):
        author(client, name)
    result = client.get("/authors/", params={"skip": 1, "limit": 1})
    assert [item["name"] for item in result.json()] == ["B"]
    assert client.get("/authors/?skip=-1").status_code == 422


def test_books_filter_pagination_and_missing_author(client):
    first = author(client, "A").json()["id"]
    second = author(client, "B").json()["id"]
    assert book(client, first, "One").status_code == 201
    assert book(client, second, "Other").status_code == 201
    created = book(client, first, "Two").json()
    assert created["author_id"] == first
    assert created["publication_date"] == "2020-01-02"
    filtered = client.get("/books/", params={"author_id": first}).json()
    assert [b["title"] for b in filtered] == ["One", "Two"]
    page = client.get("/books/", params={
        "author_id": first, "skip": 1, "limit": 1
    }).json()
    assert [b["title"] for b in page] == ["Two"]
    assert client.get("/books/?author_id=999").json() == []
    assert book(client, 999, "Missing").status_code == 404
    assert client.get("/books/?skip=1&limit=1").json()[0]["title"] == "Other"


def test_invalid_date_is_rejected(client):
    author_id = author(client, "A").json()["id"]
    response = client.post(f"/authors/{author_id}/books/", json={
        "title": "Book", "summary": "Summary", "publication_date": "bad"
    })
    assert response.status_code == 422
