from sqlalchemy.orm import Session
from db.models import Author, Book
import schemas


def get_all_authors(db: Session, skip: int = 0, limit: int = 100) -> list[Author]:
    return db.query(Author).offset(skip).limit(limit).all()


def get_author(db: Session, author_id: int) -> Author | None:
    return db.query(Author).filter(Author.id == author_id).first()


def get_author_by_name(db: Session, name: str) -> Author | None:
    return (
        db.query(Author).filter(Author.name == name).first()
    )


def create_author(db: Session, author: schemas.AuthorCreate) -> Author:
    db_create_author = Author(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_create_author)
    db.commit()
    db.refresh(db_create_author)
    return db_create_author


def get_book_list(
    db: Session,
    author_id: int | None = None,
    skip: int = 0,
    limit: int = 100
) -> list[Book]:
    queryset = db.query(Book)

    if author_id is not None:
        queryset = queryset.filter(Book.author_id == author_id)

    return queryset.offset(skip).limit(limit).all()


def create_book(db: Session, book: schemas.BookCreate) -> Book:
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
