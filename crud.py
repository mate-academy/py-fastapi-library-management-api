from sqlalchemy.orm import Session
from models import Author, Book
from schemas import AuthorCreate, BookCreate


def get_all_authors(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Author).offset(skip).limit(limit).all()


def get_author_by_id(id: int, db: Session):
    return db.query(Author).filter(Author.id == id).first()


def create_author(db: Session, author_data: AuthorCreate):
    author_db = Author(
        name=author_data.name,
        bio=author_data.bio,
    )
    db.add(author_db)
    db.commit()
    db.refresh(author_db)

    return author_db


def get_all_book(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Book).offset(skip).limit(limit).all()


def create_book_for_author(
        db: Session, author_id: int, book_data: BookCreate
):
    book_db = Book(
        title=book_data.title,
        summary=book_data.summary,
        publication_date=book_data.publication_date,
        author_id=author_id,
    )
    db.add(book_db)
    db.commit()
    db.refresh(book_db)

    return book_db


def get_books_author(db: Session, author_id: int):
    return db.query(Book).filter(Book.author_id == author_id).all()
