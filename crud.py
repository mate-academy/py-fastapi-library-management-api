from typing import List

from sqlalchemy.orm import Session

import models
from models import DBBook, DBAuthor
from schemas import AuthorCreate, BookCreate


def create_author(db: Session, author: AuthorCreate) -> DBAuthor:
    db_author = models.DBAuthor(
        name=author.name,
        bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_authors_with_pagination(db: Session, skip: int = 0, limit: int = 10) -> List[DBAuthor]:
    return db.query(models.DBAuthor).offset(skip).limit(limit).all()


def get_author_by_name(db: Session, name: str) -> DBAuthor:
    return db.query(models.DBAuthor).filter(models.DBAuthor.name == name).first()


def get_author_by_id(db: Session, pk: int) -> DBAuthor:
    return db.query(models.DBAuthor).filter(models.DBAuthor.id == pk).first()


def get_author_id_by_name(db: Session, name: str) -> int:
    author = db.query(models.DBAuthor).filter(models.DBAuthor.name == name).first()
    return author.id


def read_authors_list(db: Session) -> List[DBAuthor]:
    return db.query(models.DBAuthor).all()


def create_book_for_specific_author(db: Session, book: BookCreate, name: str) -> DBBook:
    author_id = get_author_id_by_name(db=db, name=name)

    db_book = models.DBBook(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book


def get_books_with_pagination(db: Session, skip: int = 0, limit: int = 0) -> List[DBBook]:
    return db.query(models.DBBook).offset(skip).limit(limit).all()


def get_book_by_title(db: Session, title: str) -> DBBook:
    return db.query(models.DBBook).filter(models.DBBook.title == title).first()


def get_filtered_books_by_author_id(db: Session, author_id: int) -> List[DBBook]:
    queryset = db.query(models.DBBook)
    queryset = queryset.filter(models.DBBook.author_id == author_id)
    return queryset.all()
