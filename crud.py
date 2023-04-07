from typing import Optional

from sqlalchemy.orm import Session

import models
import schemas


class Library:
    def __init__(self, db: Session):
        self.db = db

    def get_author_list(self, skip: int = 0, limit: int = 100) -> list[models.Author]:
        return self.db.query(models.Author).offset(skip).limit(limit).all()

    def get_author(self, author_id: int) -> Optional[models.Author]:
        return (
            self.db.query(models.Author).filter(models.Author.id == author_id).first()
        )

    def get_author_by_name(self, name: str) -> Optional[models.Author]:
        return self.db.query(models.Author).filter(models.Author.name == name).first()

    def create_author(self, author: schemas.AuthorCreate):
        db_author = models.Author(
            name=author.name,
            bio=author.name,
        )
        self.db.add(db_author)
        self.db.commit()
        self.db.refresh(db_author)
        return db_author

    def get_book_list(
            self,
            skip: int = 0,
            limit: int = 100
    ) -> list[models.Book]:
        return self.db.query(models.Book).offset(skip).limit(limit).all()

    def get_book(self, book_id: int) -> Optional[models.Book]:
        return self.db.query(models.Book).filter(models.Book.id == book_id).first()

    def get_books_by_author(self, author_id: int, skip: int = 0, limit: int = 100) -> list[models.Book]:
        return (
            self.db.query(models.Book)
            .filter(models.Book.author_id == author_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create_book(self, book: schemas.BookCreate) -> models.Book:
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

    def get_book_by_title(self, title: str) -> Optional[models.Book]:
        return self.db.query(models.Book).filter(models.Book.title == title).first()
