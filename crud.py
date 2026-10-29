from sqlalchemy.orm import Session

import schemas
from db.models import DBAuthor, DBBook


def create_authors(db: Session, author: schemas.AuthorCreate):
    new_author = DBAuthor(
        name=author.name,
        bio=author.bio
    )
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author


def list_of_authors(db: Session, skip: int = 0, limit: int = 10):
    return db.query(DBAuthor).offset(skip).limit(limit).all()


def get_author(db: Session, author_id: int):
    return db.query(DBAuthor).filter(DBAuthor.id == author_id).first()


def create_book(db: Session, book_create: schemas.BookCreate):
    new_book = DBBook(
        title=book_create.title,
        summary=book_create.summary,
        publication_date=book_create.publication_date,
        author_id=book_create.author_id
    )

    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book


def list_of_books(skip, limit, db: Session, author_id: int | None = None):
    queryset = db.query(DBBook)

    if author_id:
        queryset = queryset.filter(DBBook.author_id == author_id)

    return queryset.offset(skip).limit(limit).all()
