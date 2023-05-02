from sqlalchemy.orm import Session

from db import models
import schemas


def get_all_authors(db: Session):
    return db.query(models.DBAuthor).all()


def get_author(db: Session, author_id: int):
    return db.query(models.DBAuthor).filter(
        models.DBAuthor.id == author_id
    ).first()


def get_author_by_name(db: Session, name: str):
    return db.query(models.DBAuthor).filter(
        models.DBAuthor.name == name
    ).first()


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.DBAuthor(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_book_list(
    db: Session,
    title: str | None = None,
    summary: str | None = None,
):
    queryset = db.query(models.DBBook)

    if title:
        queryset = queryset.filter(
            models.DBBook.title.like(f"%{title}%")
        )

    if summary:
        queryset = queryset.filter(
            models.DBBook.summary.like(f"%{summary}%")
        )

    return queryset.all()


def get_book(db: Session, book_id: int):
    return db.query(models.DBBook).filter(
        models.DBBook.id == book_id
    ).first()


def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.DBBook(
        title=book.title,
        summary=book.summary,
        author_id=book.author_id,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_book_by_title(db: Session, title: str):
    return db.query(models.DBBook).filter(
        models.DBBook.title == title
    ).first()

