from sqlalchemy.orm import Session

from exceptions import AuthorNotFound, AuthorAlreadyExists, BookNotFound
from schemas import (
    AuthorCreate, AuthorUpdate,
    AuthorResponse, BookCreate,
    BookUpdate, BookResponse
)
from db.models import AuthorsModel, BooksModel


def create_author(db: Session, data: AuthorCreate) -> AuthorResponse:
    if db.query(AuthorsModel).filter(AuthorsModel.name == data.name).first():
        raise AuthorAlreadyExists(f"Author name: {data.name} already exists")

    db_author = AuthorsModel(**data.model_dump())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return AuthorResponse.model_validate(db_author)


def get_all_authors(
        db: Session,
        skip: int = 0,
        limit: int = 100) -> list[AuthorResponse]:
    db_authors = db.query(AuthorsModel).offset(skip).limit(limit).all()
    return [AuthorResponse.model_validate(author) for author in db_authors]


def get_author_by_name(db: Session, author_name: str) -> AuthorResponse:
    db_author = (
        db.query(AuthorsModel)
        .filter(AuthorsModel.name == author_name).first()
    )

    if not db_author:
        raise AuthorNotFound(f"Author name: {author_name} not found")

    return AuthorResponse.model_validate(db_author)


def get_author_by_id(db: Session, author_id: int) -> AuthorResponse:
    db_author = (
        db.query(AuthorsModel)
        .filter(AuthorsModel.id == author_id).first()
    )

    if not db_author:
        raise AuthorNotFound(f"Author ID: {author_id} not found")

    return AuthorResponse.model_validate(db_author)


def update_author(
        db: Session,
        author_id: int,
        data: AuthorUpdate) -> AuthorResponse:
    db_author = (
        db.query(AuthorsModel)
        .filter(AuthorsModel.id == author_id).first()
    )

    if not db_author:
        raise AuthorNotFound(f"Author ID: {author_id} not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(db_author, key, value)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return AuthorResponse.model_validate(db_author)


def create_book(db: Session, data: BookCreate) -> BookResponse:
    get_author_by_id(db, data.author_id)

    db_book = BooksModel(**data.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return BookResponse.model_validate(db_book)


def get_all_books(
        db: Session,
        skip: int = 0,
        limit: int = 100) -> list[BookResponse]:
    db_books = db.query(BooksModel).offset(skip).limit(limit).all()
    return [BookResponse.model_validate(book) for book in db_books]


def get_books_by_author(
        db: Session,
        author_id: int) -> list[BookResponse]:
    db_books = (
        db.query(BooksModel)
        .filter(BooksModel.author_id == author_id).all()
    )

    return [BookResponse.model_validate(book) for book in db_books]


def get_book_by_id(db: Session, book_id: int) -> BookResponse:
    db_book = db.query(BooksModel).filter(BooksModel.id == book_id).first()

    if not db_book:
        raise BookNotFound(f"Book ID: {book_id} not found")

    return BookResponse.model_validate(db_book)


def update_book(db: Session, book_id: int, data: BookUpdate) -> BookResponse:
    db_book = db.query(BooksModel).filter(BooksModel.id == book_id).first()

    if not db_book:
        raise BookNotFound(f"Book ID: {book_id} not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(db_book, key, value)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return BookResponse.model_validate(db_book)
