from sqlalchemy.orm import Session

import schemas
from models import DBAuthor, DBBook


def get_all_authors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DBAuthor).offset(skip).limit(limit).all()


def get_author(db: Session, author_id: int):
    return db.query(DBAuthor).filter(DBAuthor.id == author_id).first()


def create_author(db: Session, author):

    db_author = DBAuthor(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_all_books(
    db: Session, skip: int = 0, limit: int = 100, author_id: int | None = None
):
    query = db.query(DBBook)
    if author_id:
        query = query.filter(DBBook.author_id == author_id)
    return query.offset(skip).limit(limit).all()


def create_book(db: Session, book: schemas.BookCreate, author_id: int | None = None):
    final_author_id = author_id if author_id is not None else book.author_id

    db_book = DBBook(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=final_author_id,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
