from sqlalchemy.orm import Session

from db.models import Book, Author
from schemas import BookSchemaCreate, AuthorSchemaCreate


def create_book(db: Session, author_id: int, book: BookSchemaCreate):
    db_book = Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_book(db: Session, book_id: int):
    return db.query(Book).filter(Book.id == book_id).first()


def get_books(db: Session, author_id: int | None = None, limit: int = 0, offset: int = 0):
    queryset = db.query(Book)

    if author_id is not None:
        queryset = queryset.filter(Book.author.has(id=author_id))

    return queryset.offset(offset).limit(limit).all()


def create_author(db: Session, author: AuthorSchemaCreate):
    db_author = Author(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_author(db: Session, author_id: int):
    return db.query(Author).filter(Author.id == author_id).first()


def get_authors(db: Session, limit: int = 0, offset: int = 0):
    return db.query(Author).limit(limit).offset(offset).all()


def get_author_by_name(db: Session, author_name: str):
    return db.query(Author).filter(Author.name == author_name).first()
