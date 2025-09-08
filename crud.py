from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
import models
import schemas


def get_all_authors(skip: int, limit: int, db: Session) -> list[models.Author]:
    return db.query(models.Author).offset(skip).limit(limit).all()


def create_author(db: Session, author_schema: schemas.AuthorCreateSchema) -> models.Author:
    author = models.Author(name=author_schema.name, bio=author_schema.bio)
    db.add(author)
    try:
        db.commit()
        db.refresh(author)
        return author
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Author with this name already exists")


def get_author(db: Session, author_id: int) -> models.Author:
    return db.get(models.Author, author_id)


def get_author_by_name(db: Session, name: str) -> models.Author:
    return db.query(models.Author).filter(models.Author.name == name).first()


def get_all_books(skip: int, limit: int, db: Session, author_id: int | None = None) -> list[models.Book]:
    query = db.query(models.Book)
    if author_id is not None:
        query = query.filter(models.Book.author_id == author_id)
    return query.offset(skip).limit(limit).all()


def get_book(db: Session, book_id: int) -> models.Book:
    return db.get(models.Book, book_id)


def create_book(author_id: int, book_schema: schemas.BookCreateSchema, db: Session) -> models.Book:
    book = models.Book(
        title=book_schema.title,
        summary=book_schema.summary,
        publication_date=book_schema.publication_date,
        author_id=author_id
    )
    db.add(book)
    try:
        db.commit()
        db.refresh(book)
        return book
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Book creation failed due to invalid author_id or duplicate")
