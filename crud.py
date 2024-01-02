from sqlalchemy.orm import Session
from db import models
from schemas import AuthorCreate, BookCreate
from sqlalchemy import select


def get_all_authors(db: Session, skip: int = 0, limit: int = 10):
    query = select(models.Author).offset(skip).limit(limit)
    return db.execute(query).scalars().all()


def get_authors_by_name(db: Session, name: str):
    query = select(models.Author).filter(models.Author.name == name)
    return db.execute(query).scalars().first()


def get_author(db: Session, author_id: int):
    query = select(models.Author).filter(models.Author.id == author_id)
    return db.execute(query).scalars().first()


def create_author(db: Session, author: AuthorCreate):
    db_author = models.Author(
        name=author.name,
        bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_all_books(db: Session,
                  author_id: int | None = None,
                  skip: int = 0,
                  limit: int = 10):
    queryset = select(models.Book)

    if author_id:
        queryset = queryset.where(models.Book.author_id == author_id)

    queryset = queryset.offset(skip).limit(limit)

    return db.execute(queryset).scalars().all()


def create_book(db: Session, book: BookCreate):
    db_book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
