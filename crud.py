from sqlalchemy import select
from sqlalchemy.orm import Session

from db.models import Author, Book
from db.schemas import AuthorCreate, BookCreate


def get_all_authors_by_skip_and_limit(db: Session, skip: int, limit: int):
    authors = db.scalars(select(Author)).all()
    return authors[skip:skip + limit]

def create_new_author(db: Session, author: AuthorCreate):
    db_author = Author(name=author.name, bio=author.bio)

    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author

def get_author_by_id(db: Session, item_id: int):
    stmt = select(Author).where(Author.id == item_id)

    result = db.execute(stmt)
    return result.scalars().first()

def create_book_for_author(db: Session, book: BookCreate):
    db_book = Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id
    )

    db.add(db_book)
    db.commit()

    db.refresh(db_book)

    return db_book


def get_books_by_skip_limit(db: Session, skip: int, limit: int):
    db_books = db.scalars(select(Book)).all()
    return db_books[skip:skip + limit]


def retrieve_book_by_id(db: Session, item_id: int):
    stmt = select(Book).where(Book.id == item_id)

    result = db.execute(stmt)
    return result.scalars().first()
