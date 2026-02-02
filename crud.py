from typing import Sequence, Any, Type

from sqlalchemy import select, Row, RowMapping, or_
from sqlalchemy.orm import Session
from sqlalchemy.sql import func, Select

from models import DBAuthor, DBBook
from schemas import AuthorCreate, BookCreate


def paginate(db: Session, query: Select, page: int, size: int):
    skip = (page - 1) * size
    total = db.scalar(select(func.count()).select_from(query.subquery()))
    results = db.scalars(query.offset(skip).limit(size)).all()

    return {
        "total": total,
        "page": page,
        "size": size,
        "results": results
    }


def get_all_authors(
        db: Session,
        page: int = 1,
        size: int = 10,
        name: str | None = None,
) -> Sequence[Row[Any] | RowMapping | Any]:
    query = select(DBAuthor)
    if name:
        query = query.where(
            DBAuthor.name.ilike(f"%{name}%")
        )
    return paginate(db=db, query=query, page=page, size=size)


def create_author(db: Session, author: AuthorCreate) -> DBAuthor:
    db_author = DBAuthor(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_author_by_id(db: Session, author_id: int) -> DBAuthor:
    return db.scalar(select(DBAuthor).where(DBAuthor.id == author_id))


def get_author_by_name(db: Session, author_name: str) -> DBAuthor:
    return db.scalar(select(DBAuthor).where(DBAuthor.name == author_name))


def get_all_books(
        db: Session,
        page: int = 1,
        size: int = 10,
        title: str | None = None,
        author_id: int | None = None,
) -> Sequence[Row[Any] | RowMapping | Any]:
    query = select(DBBook)
    if title:
        query = query.where(DBBook.title.ilike(f"%{title}%"))
    if author_id:
        query = query.where(DBBook.author_id == author_id)
    return paginate(db=db, query=query, page=page, size=size)


def get_book_by_id(db: Session, book_id: int) -> DBBook:
    return db.scalar(select(DBBook).where(DBBook.id == book_id))


def get_book_by_title_and_author(db: Session, book_title: str,
                                 book_author: int) -> DBBook:
    return db.scalar(select(DBBook).where(
        (DBBook.title == book_title) & (DBBook.author_id == book_author)
    ))


def create_book(db: Session, book: BookCreate) -> DBBook:
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
