from sqlalchemy.orm import Session

from . import models, schemas


def get_authors(db: Session):
    return db.query(models.Author).all()


def get_author(db: Session, author_id: int):
    return db.query(models.Author).filter(models.Author.id == author_id).first()


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_books(db: Session):
    return db.query(models.Book).all()


def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def create_book(db: Session, book: schemas.BookCreate, author_ids: list[int]):
    db_book = models.Book(title=book.title, summary=book.summary)
    db.add(db_book)
    for author_id in author_ids:
        db_author = db.query(models.Author).filter(models.Author.id == author_id).first()
        db_book.author.append(db_author)
    db.commit()
    db.refresh(db_book)
    return db_book
