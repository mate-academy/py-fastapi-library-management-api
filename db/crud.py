from sqlalchemy.orm import Session

import models
import schemas


def get_all_books(db: Session):
    return db.query(models.DBBook).all()


def get_book_by_title(db: Session, title: str):
    return (
        db.query(models.DBBook).filter(models.DBBook.title == title).first()
    )


def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.DBBook(
        title=book.title,
        summary=book.summary,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book


def get_author_list(
    db: Session,
    books: str | None = None,
):
    queryset = db.query(models.DBAuthor)

    if books is not None:
        queryset = queryset.filter(models.DBAuthor.books.any(title=books))

    return queryset.all()


def get_author(db: Session, author_id: int):
    return db.query(models.DBAuthor).filter(models.DBAuthor.id == author_id).first()


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.DBAuthor(
        name=author.name,
        bio=author.bio,
        book_id=author.book_id,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author
