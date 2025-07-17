from sqlalchemy.orm import Session

from models import Author, Book


def get_all_authors(db: Session):
    return db.query(Author).all()


def get_books(db: Session):
    return db.query(Book).all()
