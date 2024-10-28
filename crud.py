from sqlalchemy.orm import Session

from models import DBAuthor, DBBook
import schemas


def get_all_authors(db: Session, skip: int = 0, limit: int = 10):
    return db.query(DBAuthor).offset(skip).limit(limit).all()


def get_author_by_id(db: Session, author_id: int):
    return db.query(DBAuthor).filter(DBAuthor.id == author_id).first()


def get_author_by_name(db: Session, author_name: str):
    return db.query(DBAuthor).filter(DBAuthor.name == author_name).first()


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = DBAuthor(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()

    db.refresh(db_author)
    return db_author


def create_book(db: Session, book: schemas.BookCreate, author_id: int):
    db_book = DBBook(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_books(db: Session, skip: int = 0, limit: int = 10):
    return db.query(DBBook).offset(skip).limit(limit).all()


def get_books_by_author(db: Session, author_id: int):
    return db.query(DBBook).filter(DBBook.author_id == author_id).all()
