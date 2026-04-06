from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Author, Book
from schemas import AuthorCreateSchema, BookCreateSchema

"""FUNCTIONS FOR AUTHOR ENDPOINTS"""
def create_author(data: AuthorCreateSchema, db: Session) -> Author:
    author = Author(
        name=data.name,
        bio=data.bio,
    )

    db.add(author)
    db.commit()
    db.refresh(author)

    return author


def get_list_author_from_db(db: Session, skip: int = 0 , limit: int = 10):
    authors = db.execute(select(Author).offset(skip).limit(limit)).scalars().all()
    return [author for author in authors]


def get_author_by_id_from_db(author_id: int, db: Session):
    return db.execute(select(Author).where(Author.id == author_id)).scalars().first()


"""FUNCTIONS FOR BOOK ENDPOINTS"""
def add_book_to_db(data: BookCreateSchema, db: Session) -> Book:
    book = Book(
        title=data.title,
        summary=data.summary,
        publication_date=data.publication_date,
        author_id=data.author_id
    )

    db.add(book)
    db.commit()
    db.refresh(book)

    return book


def get_list_books_from_db(db: Session, skip: int = 0 , limit: int = 10):
    books = db.execute(select(Book).offset(skip).limit(limit)).scalars().all()
    return [book for book in books]


def get_book_by_author_id_from_db(author_id: int, db: Session):
    request = db.execute(select(Book).where(Book.author_id == author_id))
    books = request.scalars().all()
    return [book for book in books]
