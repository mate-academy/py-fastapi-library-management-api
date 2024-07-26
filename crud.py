from sqlalchemy.orm import Session

import models
import schemas
from pagination import paginate


def get_authors_list(skip: int, limit: int, db: Session):
    author_queryset = db.query(models.DBAuthor)
    return paginate(author_queryset, skip=skip, limit=limit)


def get_author_by_name(db: Session, name: str):
    return db.query(models.DBAuthor).filter(models.DBAuthor.name == name).first()


def get_author_by_id(db: Session, author_id: int):
    return db.query(models.DBAuthor).filter(models.DBAuthor.id == author_id).first()


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.DBAuthor(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_books_list(
    skip: int,
    limit: int,
    db: Session,
    author_id: int | None = None,
):
    book_queryset = db.query(models.DBBook)

    if author_id is not None:
        book_queryset = book_queryset.filter(models.DBBook.author_id == author_id)

    return paginate(book_queryset, skip=skip, limit=limit)


def get_book(db: Session, book_id: int):
    return db.query(models.DBBook).filter(models.DBBook.id == book_id).first()


def validate_author_id(db: Session, author_id: int):
    author = db.query(models.DBAuthor).filter(models.DBAuthor.id == author_id).first()
    if not author:
        return True
    return False


def create_book(db: Session, book: schemas.BookCreate):
    db_cheese = models.DBBook(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id,
    )
    db.add(db_cheese)
    db.commit()
    db.refresh(db_cheese)
    return db_cheese
