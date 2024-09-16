from sqlalchemy.orm import Session
import models
import schemas


def get_author(db: Session, author_id: int):
    author = db.query(models.DBAuthor).filter(models.DBAuthor.id == author_id).first()
    return author


def get_authors(db: Session, skip: int = 0, limit: int = 10):
    authors = db.query(models.DBAuthor).offset(skip).limit(limit).all()
    return authors


def get_books_by_author(db: Session, author_id: int, skip: int = 0, limit: int = 10):
    books = db.query(models.DBBook).filter(models.DBBook.author_id == author_id).offset(skip).limit(limit).all()
    return books


def get_books(db: Session, skip: int = 0, limit: int = 10):
    books = db.query(models.DBBook).offset(skip).limit(limit).all()
    return books


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.DBAuthor(
        name=author.name,
        bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.DBBook(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
