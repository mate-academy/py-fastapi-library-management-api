from sqlalchemy.orm import Session

from models import Author, Book
from schemas import AuthorCreate, BookCreate


def create_author(db: Session, author: AuthorCreate):
    db_author = Author(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author

def get_all_authors(db: Session):
    return db.query(Author).all()

def get_author_by_id(db: Session, author_id: int):
    return db.query(Author).filter(Author.id == author_id).first()

def create_book(db: Session, book: BookCreate):
    db_book = Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book

def get_all_books(db: Session):
    return db.query(Book).all()

def get_books_by_author_id(db: Session, author_id: int):
    return db.query(Book).filter(Book.author_id == author_id).all()
