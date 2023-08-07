from sqlalchemy.orm import Session
import models
import schemas


def get_author_by_name(db: Session, author_name: str):
    return db.query(models.Author).filter(author_name == models.Author.name).first()


def get_author(db: Session, author_id: int):
    return db.query(models.Author).filter(author_id == models.Author.id).first()


def get_authors(db: Session, skip: int = 0, limit: int = 5):
    return db.query(models.Author).offset(skip).limit(limit).all()


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(book_id == models.Book.id).first()


def get_books(db: Session, skip: int = 0, limit: int = 10, author_id: int = None):
    query = db.query(models.Book)
    if author_id:
        query = query.filter(author_id == models.Book.author_id)
    return query.offset(skip).limit(limit).all()


def create_book(db: Session, book: schemas.BookCreate, author_id: int):
    db_book = models.Book(
        **book.dict(), author_id=author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
