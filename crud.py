from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
import models
import schemas


def create_new_author(db: Session, author: schemas.AuthorCreateSchema):
    author = models.Author(
        name=author.name,
        bio=author.bio
    )
    db.add(author)
    db.commit()
    db.refresh(author)

    return author


def get_all_authors_with_pagination(db: Session, skip: int = 0, limit: int = 10):
    return (
        db.query(models.Author)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_all_books_with_pagination(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        author_id: int | None = None):
    stmt = select(models.Book)
    if author_id is not None:
        stmt = stmt.where(models.Book.author_id == author_id)
    stmt = stmt.offset(skip).limit(limit)

    return db.scalars(stmt).all()


def get_author_by_id(db: Session, author_id: int):
    author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


def add_book_by_author_id(db: Session, author_id: int, book: schemas.BookCreateSchema):
    author = db.get(models.Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    book = models.Book(title=book.title,
                       summary=book.summary,
                       publication_date=book.publication_date,
                       author_id=author_id)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book
