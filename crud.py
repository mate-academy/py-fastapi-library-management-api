from sqlalchemy.orm import Session

from models import Book
from schemas import BookBase


def get_all_books(db: Session):
    return db.query(Book).all()


def get_book_by_id(db: Session, id: int):
    return db.query(Book).filter(Book.id == id).first()



def create_book(db: Session, data: BookBase):
    db_book = Book(**data.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
