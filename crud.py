from sqlalchemy import select
from sqlalchemy.orm import Session

from db.models import DBAuthor, DBBook
import schemas


def get_all_authors(
    db: Session,
    skip: int = 0,
    limit: int = 100
) -> list[DBAuthor]:
    return db.scalars(
        select(DBAuthor).offset(skip).limit(limit)
    ).all()


def create_author(db: Session, author: schemas.AuthorCreate) -> DBAuthor:
    db_author = DBAuthor(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_author_by_id(db: Session, author_id: int) -> DBAuthor | None:
    return db.scalars(
        select(DBAuthor).where(DBAuthor.id == author_id)
    ).first()


def get_author_by_name(db: Session, name: str) -> DBAuthor | None:
    return db.scalars(select(DBAuthor).where(DBAuthor.name == name)).first()


def get_all_books(
    db: Session,
    skip: int = 0,
    limit: int = 100
) -> list[DBBook]:
    return db.scalars(
        select(DBBook).offset(skip).limit(limit)
    ).all()


def create_book(db: Session, book: schemas.BookCreate) -> DBBook:
    db_book = DBBook(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_book_by_author_id(db: Session, author_id: int) -> list[DBBook]:
    return db.scalars(
        select(DBBook).where(DBBook.author_id == author_id)
    ).all()
