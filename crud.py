from sqlalchemy.orm import Session

from models import Book, Author
from schemas import BookBase, AuthorBase


def get_all_books(db: Session, author_id: int | None = None):
    query = db.query(Book)

    if author_id:
        query = query.filter(Book.author_id == author_id)

    return query.all()


def get_book_by_id(db: Session, id: int):
    return db.query(Book).filter(Book.id == id).first()


def create_book(db: Session, data: BookBase):
    db_book = Book(**data.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_authors(db: Session):
    return db.query(Author).all()


def get_author_by_id(db: Session, id: int):
    return db.query(Author).filter(Author.id == id).first()


def get_author_by_name(db: Session, name: str):
    return db.query(Author).filter(Author.name == name).first()


def create_author(db: Session, data: AuthorBase):
    db_author = Author(**data.model_dump())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author
