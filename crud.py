from sqlalchemy.orm import Session

from models import Author, Book
from schemas import AuthorCreate, BookCreate


def get_authors_list(db: Session, skip: int = 0, limit: int = 20):
    queryset = db.query(Author).offset(skip).limit(limit).all()

    return queryset


def get_author(author_id: int, db: Session):
    queryset = db.query(Author).filter(Author.id == author_id).first()
    return queryset


def create_author(author: AuthorCreate, db: Session):
    existing = db.query(Author).filter(Author.name == author.name).first()
    if existing:
        return None

    new_author = Author(**author.model_dump())
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author


def get_books_list(
    db: Session, author_id: int | None = None, skip: int = 0, limit: int = 20
):
    queryset = db.query(Book)

    if author_id:
        queryset = queryset.filter(Book.author_id == author_id)

    return queryset.offset(skip).limit(limit).all()


def get_book(book_id: int, db: Session):
    queryset = db.query(Book).filter(Book.id == book_id).first()
    return queryset


def create_book(book: BookCreate, db: Session):
    author_exists = db.query(Author).filter(Author.id == book.author_id).first()
    if not author_exists:
        return None

    new_book = Book(**book.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book
