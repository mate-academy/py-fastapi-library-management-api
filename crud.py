from sqlalchemy import select
from sqlalchemy.orm import Session
from models import Author, Book
from schemas import AuthorCreate, BookCreate


def get_all_authors(db: Session, skip: int = 0, limit: int = 10):
    return db.scalars(
        select(Author).offset(skip).limit(limit)
    ).all()

def get_author_name(db: Session, name: str = None):
    return db.scalar(select(Author).where(Author.name == name))

def get_author(db: Session, author_id: int):
    return db.scalar(select(Author).where(Author.id == author_id))

def create_author(db: Session, author: AuthorCreate):
    db_author = Author(
        name=author.name,
        bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

def get_all_books(
        db: Session,
        title: str = None,
        author_id: int = None,
        skip: int = 0,
        limit: int = 10
        ):
    stmt = select(Book)

    if title is not None:
        stmt = stmt.where(Book.title == title)

    if author_id is not None:
        stmt = stmt.join(Author).where(Author.id == author_id)

    stmt = stmt.offset(skip).limit(limit)

    return db.scalars(stmt).all()

def get_book(db: Session, book_id: int):
    return db.scalar(select(Book).where(Book.id == book_id))

def create_book(db: Session, book: BookCreate):
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
