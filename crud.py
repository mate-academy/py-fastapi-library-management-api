from typing import List, Union
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

from pydantic import BaseModel
from datetime import date
from schemas import AuthorCreate, BookCreate


class DBSession:
    def __init__(self):
        self._session = None
    def __enter__(self):
        self._session = SessionLocal()
        return self._session

    def __exit__(self, exc_type, exc_value, traceback):
        self._session.close()


def get_db() -> Session:
    with DBSession() as db:
        yield db


class BookService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_all_author(
            self,
            skip: int = 0,
            limit: int = 100,
    ) -> List[models.Author]:
        return self.db.query(models.Author).offset(skip).limit(limit).all()

    def create_author(self, author: AuthorCreate):
        db_author = models.Author(name=author.name, bio=author.bio)
        self.db.add(db_author)
        self.db.commit()
        self.db.refresh(db_author)
        return db_author

    def get_author(self, author_id: int):
        return self.db.query(models.Author).filter(models.Author.id == author_id).first()

    def get_books(self, author_id: Union[int, None] = None,  skip: int = 0, limit: int = 100, ) -> List[models.Book]:
        queryset = self.db.query(models.Book)
        if author_id is not None:
            queryset = queryset.filter(models.Book.author_id == author_id)
        return queryset.offset(skip).limit(limit).all()

    def create_book(self, book: BookCreate):
        db_book = models.Book(
            title=book.title,
            summary=book.summary,
            publication_date=book.publication_date,
            author_id=book.author_id,
        )
        self.db.add(db_book)
        self.db.commit()
        self.db.refresh(db_book)
        return db_book
