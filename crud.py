from sqlalchemy.orm import Session
import models
import schemas


def get_authors(db: Session, author_id: int = None, skip: int = 0, limit: int = 10):
    if author_id:
        authors = db.query(models.DBAuthor).filter(models.DBAuthor.id == author_id).first()
    else:
        authors = db.query(models.DBAuthor).offset(skip).limit(limit).all()
    return authors


def get_books(db: Session, author_id: int = None, skip: int = 0, limit: int = 10):
    if author_id:
        books = db.query(models.DBBook).filter(models.DBBook.author_id == author_id).offset(skip).limit(limit).all()
    else:
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
