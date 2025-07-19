from datetime import datetime
from typing import Annotated, List, Type

from fastapi import Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from db.models import Author, Book
import schemas
import db.models as models


def get_author_by_name(session: Session, name: str):
    return session.query(models.Author).filter(models.Author.name == name).first()


def get_author_by_id(session: Session, author_id: int):
    statement = select(Author).where(Author.id == author_id)
    return session.exec(statement).first()


def create_author(session: Session, author_data: schemas.AuthorBaseSchema):
    author = Author(name=author_data.name, bio=author_data.bio)
    session.add(author)
    session.commit()
    session.refresh(author)
    return author


def get_list_author(
        session: Session,
        skip: int,
        limit: int,
) -> list[Type[Author]]:
    return session.query(models.Author).offset(skip).limit(limit).all()


def create_book(session: Session, book: schemas.BookBaseSchema):
    book = Book(
        title=book.title,
        summary=book.summary,
        author_id=book.author_id,
        publication_date=datetime.strptime(book.publication_date, "%Y-%m-%d").date(),
    )
    session.add(book)
    session.commit()
    session.refresh(book)
    return book
