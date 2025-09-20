from typing import Sequence, Type
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import select, Select
from fastapi.exceptions import HTTPException
from fastapi import status

from models import DbAuthor, DbBook
from schemas import AuthorCreate, BookCreate


def get_basic_selection(model: Type[DeclarativeBase]) -> Select:
    return select(model)

def filter_by_author_id(selection: Select, author_id: int) -> Select:
    return selection.where(DbBook.author_id==author_id)

def paginate(selection: Select, skip: int, limit: int) -> Select:
    return selection.offset(skip).limit(limit)



def get_all_authors(db: Session, skip: int, limit: int) -> Sequence[DbAuthor]:
    return db.execute(
        paginate(
            selection=get_basic_selection(DbAuthor),
            skip=skip,
            limit=limit
        )
    ).scalars().all()


def get_author_by_name(db: Session, author_name: str) -> DbAuthor | None:
    return db.query(DbAuthor).filter(DbAuthor.name == author_name).first()

def get_author_by_id(db: Session, author_id: int) -> DbAuthor | None:
    return db.query(DbAuthor).filter(DbAuthor.id == author_id).first()


def add_author_to_db(db: Session, author: AuthorCreate) -> DbAuthor:
    db_author = DbAuthor(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

def delete_author(db: Session, author_id: int) -> None:
    db_author = db.query(DbAuthor).filter(DbAuthor.id == author_id).first()
    if not db_author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Author not found"
        )
    db.delete(db_author)
    db.commit()


def get_all_books(
        db: Session,
        skip: int,
        limit: int,
        author_id: int | None
) -> Sequence[DbBook]:
    selection = get_basic_selection(DbBook)
    if author_id is not None:
        selection = filter_by_author_id(selection, author_id)
    return db.execute(
        paginate(
            selection=selection,
            skip=skip,
            limit=limit
        )
    ).scalars().all()


def add_book_to_db(db: Session, book: BookCreate) -> DbBook:
    author = get_author_by_id(db=db, author_id=book.author_id)
    if author is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Author not found"
        )
    db_book = DbBook(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int) -> None:
    db_book = db.query(DbBook).filter(DbBook.id == book_id).first()
    if db_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    db.delete(db_book)
    db.commit()
