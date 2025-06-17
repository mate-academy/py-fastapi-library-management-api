import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date

from database import Base
import models
import crud
import schemas

SQLALCHEMY_DATABASE_URL_TEST = "sqlite:///:memory:"

@pytest.fixture(name="db_session")
def db_session_fixture():
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL_TEST,
        connect_args={"check_same_thread": False}
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

def test_create_author(db_session):
    author_data = schemas.AuthorCreate(name="Тарас Шевченко", bio="Видатний український поет.")
    author = crud.create_author(db_session, author_data)

    assert author is not None # Перевіряємо, що автор був успішно створений
    assert author.id is not None
    assert author.name == "Тарас Шевченко" # Очікуємо оригінальний регістр
    assert author.bio == "Видатний український поет."

    # ДОДАНО: Тест на створення дубліката (регістронезалежно)
    duplicate_author_data = schemas.AuthorCreate(name="тарас шевченко", bio="Ще один поет.")
    duplicate_author = crud.create_author(db_session, duplicate_author_data)
    assert duplicate_author is None # Очікуємо None, оскільки це дублікат

def test_get_author(db_session):
    author_data = schemas.AuthorCreate(name="Іван Франко", bio="Великий український письменник.")
    created_author = crud.create_author(db_session, author_data)

    found_author = crud.get_author(db_session, created_author.id)
    assert found_author is not None
    assert found_author.name == "Іван Франко" # Очікуємо оригінальний регістр
    assert found_author.id == created_author.id

def test_get_author_by_name(db_session):
    author_data = schemas.AuthorCreate(name="Леся Українка", bio="Видатна українська поетеса.")
    crud.create_author(db_session, author_data)

    found_author_lower = crud.get_author_by_name(db_session, "леся українка")
    assert found_author_lower is not None
    assert found_author_lower.name == "Леся Українка" # Очікуємо оригінальний регістр

    found_author_upper = crud.get_author_by_name(db_session, "ЛЕСЯ УКРАЇНКА")
    assert found_author_upper is not None
    assert found_author_upper.name == "Леся Українка" # Очікуємо оригінальний регістр

    found_author_mixed = crud.get_author_by_name(db_session, "ЛеСя УкРаЇнКа")
    assert found_author_mixed is not None
    assert found_author_mixed.name == "Леся Українка" # Очікуємо оригінальний регістр

    not_found_author = crud.get_author_by_name(db_session, "Володимир Винниченко")
    assert not_found_author is None

def test_get_authors(db_session):
    crud.create_author(db_session, schemas.AuthorCreate(name="Василь Стус", bio="Поет-дисидент."))
    crud.create_author(db_session, schemas.AuthorCreate(name="Ліна Костенко", bio="Сучасна українська поетеса."))

    authors = crud.get_authors(db_session)
    assert len(authors) == 2
    assert "Василь Стус" in [a.name for a in authors] # Очікуємо оригінальний регістр
    assert "Ліна Костенко" in [a.name for a in authors] # Очікуємо оригінальний регістр

    paginated_authors = crud.get_authors(db_session, skip=1, limit=1)
    assert len(paginated_authors) == 1
    assert paginated_authors[0].name in ["Василь Стус", "Ліна Костенко"] # Очікуємо оригінальний регістр

def test_create_book(db_session):
    author_data = schemas.AuthorCreate(name="Григорій Сковорода", bio="Філософ.")
    author = crud.create_author(db_session, author_data)

    book_data = schemas.BookCreate(
        title="Байки Харківські",
        summary="Збірка філософських байок.",
        publication_date=date(1774, 1, 1)
    )
    book = crud.create_book(db_session, book_data, author.id)

    assert book.id is not None
    assert book.title == "Байки Харківські"
    assert book.author_id == author.id

def test_get_book(db_session):
    author_data = schemas.AuthorCreate(name="Олександр Довженко", bio="Кінорежисер.")
    author = crud.create_author(db_session, author_data)

    book_data = schemas.BookCreate(
        title="Зачарована Десна",
        summary="Автобіографічна повість.",
        publication_date=date(1957, 1, 1)
    )
    created_book = crud.create_book(db_session, book_data, author.id)

    found_book = crud.get_book(db_session, created_book.id)
    assert found_book is not None
    assert found_book.title == "Зачарована Десна"
    assert found_book.id == created_book.id

def test_get_books(db_session):
    author1_data = schemas.AuthorCreate(name="Микола Гоголь", bio="Письменник.")
    author1 = crud.create_author(db_session, author1_data)
    crud.create_book(db_session, schemas.BookCreate(title="Вечори на хуторі біля Диканьки", summary="", publication_date=date(1832, 1, 1)), author1.id)
    crud.create_book(db_session, schemas.BookCreate(title="Мертві душі", summary="", publication_date=date(1842, 1, 1)), author1.id)

    author2_data = schemas.AuthorCreate(name="Пантелеймон Куліш", bio="Письменник.")
    author2 = crud.create_author(db_session, author2_data)
    crud.create_book(db_session, schemas.BookCreate(title="Чорна рада", summary="", publication_date=date(1857, 1, 1)), author2.id)

    all_books = crud.get_books(db_session)
    assert len(all_books) == 3

    author1_books = crud.get_books(db_session, author_id=author1.id)
    assert len(author1_books) == 2
    assert author1_books[0].title == "Вечори на хуторі біля Диканьки"

    author2_books = crud.get_books(db_session, author_id=author2.id)
    assert len(author2_books) == 1
    assert author2_books[0].title == "Чорна рада"

    paginated_books = crud.get_books(db_session, skip=1, limit=1)
    assert len(paginated_books) == 1
