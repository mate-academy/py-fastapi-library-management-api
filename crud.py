from sqlalchemy import select
from sqlalchemy.orm import Session
import models
from schemas import AuthorCreate, BookCreate


def create_author(db: Session, author: AuthorCreate):
    db_author = models.Author(
        name=author.name,
        bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_all_authors(db: Session, skip: int = 0, limit: int = 10):
    queryset = (
        select(models.Author)
        .offset(skip)
        .limit(limit)
    )
    return db.scalars(queryset).all()


def get_author_by_id(db: Session, author_id: int) -> models.Author | None:
    return db.scalar(select(models.Author).where(models.Author.id == author_id))


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


def get_all_books(db: Session, skip: int = 0, limit: int = 10):
    queryset = (
        select(models.Book)
        .offset(skip)
        .limit(limit)
    )
    return db.scalars(queryset).all()


def get_book_list(
    db: Session,
    author_id: int | None = None,
) -> list[models.Book]:
    queryset = select(models.Book)

    if author_id:
        queryset = queryset.where(models.Book.author_id == author_id)

    return db.scalars(queryset).all()


def get_author_by_name(db: Session, name: str) -> models.Author | None:
    return db.scalar(
        select(models.Author).where(models.Author.name == name)
    )
