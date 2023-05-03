from sqlalchemy.orm import Session
from db import models

import schemas


def get_author(db: Session, author_id: int):
    return db.query(models.Author).filter(models.Author.id == author_id).first()


def get_all_authors(db: Session):
    return db.query(models.Author).all()


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def get_all_books(db: Session):
    return db.query(models.Book).all()


# book_publication_date_str = book_publication_date.strftime("%Y-%m-%d")
# create_book(
#     db, BookCreate(
#         title="book title",
#         summary="book summary",
#         author_id=1,
#         publication_date=book_publication_date_str
#     )
# )


def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(
        title=book.title,
        summary=book.summary,
        author_id=book.author_id
    )
    db_book.set_publication_date(book.publication_date)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
