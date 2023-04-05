from typing import List
from sqlalchemy import and_
from sqlalchemy.orm import Session

from models import Author, Book
import schemas


class BookService:
    def __init__(self, db: Session):
        self.db: Session = db

    def get_all_authors(
            self,
            skip: int = 0,
            limit: int = 10
    ) -> List[Author]:
        return self.db.query(Author).offset(skip).limit(limit).all()

    def get_author_by_name(self, name: str) -> Author:
        return self.db.query(Author).filter(
            and_(Author.name == name)
        ).first()

    def get_author_by_id(self, author_id: int) -> Author:
        return self.db.query(Author).filter(
            and_(Author.id == author_id)
        ).first()

    def create_author(self, author: schemas.AuthorCreate) -> Author:
        db_author = Author(
            name=author.name,
            bio=author.bio,
        )
        self.db.add(db_author)
        self.db.commit()
        self.db.refresh(db_author)

        return db_author

    def get_book_list(
            self,
            skip: int = 0,
            limit: int = 10,
            author: str | None = None
    ) -> List[Book]:
        queryset = self.db.query(Book)

        if author is not None:
            queryset = queryset.filter(Book.author.has(name=author))

        return queryset.offset(skip).limit(limit).all()

    def create_book(self, book: schemas.BookCreate) -> Book:
        db_book = Book(
            title=book.title,
            summary=book.summary,
            publication_date=book.publication_date,
            author_id=book.author_id,
        )
        self.db.add(db_book)
        self.db.commit()
        self.db.refresh(db_book)

        return db_book
