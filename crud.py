from sqlalchemy import select
from sqlalchemy.orm import Session
from models import DBBook, DBAuthor
from schemas import BookCreate, AuthorCreate


def get_all_books(db: Session, author_id: int | None = None):
    queryset = select(DBBook)

    if author_id is not None:
        queryset = queryset.filter(DBBook.author_id == author_id)

    return db.scalars(queryset).all()


def get_book(db: Session, book_id: int):
    return db.scalar(select(DBBook).where(DBBook.id == book_id))


def create_book(db: Session, book: BookCreate):
    db_book = DBBook(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_book_by_title(db: Session, title: str):
    return db.scalar(select(DBBook).where(DBBook.title == title))


def get_all_authors(db: Session, skip: int = 0, limit: int = 100):
    return db.scalars(select(DBAuthor)).offset(skip).limit(limit).all()


def get_author(db: Session, author_id: int):
    return db.scalar(select(DBAuthor).where(DBAuthor.id == author_id))


def create_author(db: Session, author: AuthorCreate):
    db_author = DBAuthor(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_author_by_name(db: Session, name: str):
    return db.scalar(select(DBAuthor).where(DBAuthor.name == name))
