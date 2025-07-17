from sqlalchemy.orm import Session

from models import Author, Book


def get_all_authors(skip, limit, db: Session):
    return db.query(Author).offset(skip).limit(limit).all()


def get_all_books(skip, limit, db: Session):
    return db.query(Book).offset(skip).limit(limit).all()
