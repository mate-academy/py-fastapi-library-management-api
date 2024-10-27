import schemas
from sqlalchemy.orm import Session
from models import Author, Book


# Author CRUD Functions
def get_all_authors(db: Session) -> list[Author]:
    return db.query(Author).all()


def get_author_by_name(db: Session, name: str) -> Author:
    return (
        db.query(Author).filter(Author.name == name).first()
    )


def get_author_by_id(db: Session, id: int) -> Author:
    return (
        db.query(Author).filter(Author.id == id).first()
    )


def create_author(db: Session, author: schemas.AuthorCreate) -> Author:
    db_author = Author(
        name=author.name,
        bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def update_author(
        db: Session,
        author_id: int,
        author_data: schemas.AuthorUpdate
) -> Author | None:
    db_author = db.query(Author).filter(Author.id == author_id).first()
    if not db_author:
        return None

    for key, value in author_data.dict(exclude_unset=True).items():
        setattr(db_author, key, value)

    db.commit()
    db.refresh(db_author)

    return db_author


def delete_author(db: Session, author_id: int) -> bool:
    db_author = db.query(Author).filter(Author.id == author_id).first()
    if not db_author:
        return False

    db.delete(db_author)
    db.commit()

    return True


# Book CRUD Functions
def get_all_books(db: Session) -> list[Book]:
    return db.query(Book).all()


def get_book_by_id(db: Session, book_id: int) -> Book:
    return (
        db.query(Book).filter(Book.id == book_id).first()
    )


def get_books_by_author(db: Session, author_id: int) -> list[Book]:
    return (
        db.query(Book).filter(Book.author_id == author_id).all()
    )


def create_book(db: Session, book: schemas.BookCreate) -> Book:
    db_book = Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book


def update_book(
        db: Session,
        book_id: int,
        book_data: schemas.BookUpdate
) -> Book | None:
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        return None

    for key, value in book_data.dict(exclude_unset=True).items():
        setattr(db_book, key, value)

    db.commit()
    db.refresh(db_book)

    return db_book


def delete_book(db: Session, book_id: int) -> bool:
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        return False

    db.delete(db_book)
    db.commit()

    return True
