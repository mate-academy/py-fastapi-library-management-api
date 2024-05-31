from sqlalchemy.orm import Session

from models import DBAuthor, DBBook
from schemas import AuthorCreate, BookCreate


def get_all_authors(db: Session, skip: int = 0, limit: int = 10) -> DBAuthor:
    return db.query(DBAuthor).offset(skip).limit(limit).all()


def get_author_by_id(db: Session, author_id: int) -> DBAuthor:
    return db.query(DBAuthor).filter(DBAuthor.id == author_id).first()


def create_author(db: Session, author: AuthorCreate) -> DBAuthor:
    db_author = DBAuthor(
        name=author.name,
        bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    if author.books:
        for book in author.books:
            db_book = DBBook(
                title=book.title,
                summary=book.summary,
                publication_date=book.publication_date,
                author_id=db_author.id
            )
            db.add(db_book)

        db.commit()

    return db_author


def get_all_books(db: Session, skip: int = 0, limit: int = 10) -> DBBook:
    return db.query(DBBook).offset(skip).limit(limit).all()


def get_book_by_author_id(db: Session, author_id: int):
    return db.query(DBBook).filter(DBBook.author_id == author_id).all()


def create_book(db: Session, book: BookCreate) -> DBBook:
    db_book = DBBook(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book
