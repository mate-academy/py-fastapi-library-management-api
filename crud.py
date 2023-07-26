from sqlalchemy.orm import Session
from models import DBAuthor, DBBook
from schemas import AuthorCreate, BookCreate


def create_author(db: Session, author: AuthorCreate):
    new_author = DBAuthor(
        name=author.name,
        bio=author.bio
    )
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author


def get_author(db: Session, author_id: int):
    return db.query(DBAuthor).filter(DBAuthor.id == author_id).first()


def get_authors(db: Session, skip: int = 0, limit: int = 10):
    return db.query(DBAuthor).offset(skip).limit(limit).all()


def get_author_by_name(db: Session, name: str) -> DBAuthor | None:
    return (
        db.query(DBAuthor).filter(DBAuthor.name == name).first()
    )


def create_book(db: Session, book: BookCreate):
    new_book = DBBook(
        title=book.title,
        bio=book.bio,
        publication_date=book.publication_date,
        author_id=book.author_id
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


def get_book(db: Session, book_id: int):
    return db.query(DBBook).filter(DBBook.id == book_id).first()


def get_books(db: Session, skip: int = 0, limit: int = 10):
    return db.query(DBBook).offset(skip).limit(limit).all()
