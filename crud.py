from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import models
import schemas


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(name=author.name, bio=author.bio)
    db.add(db_author)
    try:
        db.commit()
        db.refresh(db_author)
        return db_author
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An author with this name already exists."
        )


def get_authors(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Author).offset(skip).limit(limit).all()


def get_author(db: Session, author_id: int):
    db_author = db.query(models.Author).filter(
        models.Author.id == author_id
    ).first()
    if not db_author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Author not found"
        )
    return db_author


def create_book(db: Session, book: schemas.BookCreate, author_id: int):
    get_author(db, author_id=author_id)

    db_book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_books(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Book).offset(skip).limit(limit).all()


def get_books_by_author(db: Session, author_id: int):
    get_author(db, author_id=author_id)
    return db.query(models.Book).filter(
        models.Book.author_id == author_id
    ).all()