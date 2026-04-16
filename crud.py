from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from db.models import DBAuthor, DBBook
from schemas import AuthorCreate, BookCreate


def create_author(db: Session, author: AuthorCreate):
    db_author = DBAuthor(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_authors(db: Session, skip: int = 0, limit: int = 10):
    return db.scalars(select(DBAuthor).offset(skip).limit(limit)).all()


def get_author_by_id(db: Session, author_id: int):
    return db.scalars(select(DBAuthor).where(DBAuthor.id == author_id)).first()


def create_book(db: Session, book: BookCreate):
    db_book = DBBook(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    _ = db_book.author  # force lazy load while session is open
    return db_book


def get_books(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        author_id: int = None
):
    queryset = select(DBBook).options(selectinload(DBBook.author)).offset(skip).limit(limit)

    if author_id is not None:
        queryset = queryset.where(DBBook.author_id == author_id)

    return db.scalars(queryset).all()
