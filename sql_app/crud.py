from sqlalchemy.orm import Session

from sql_app import models, schemas


def create_author(db: Session, author: schemas.AuthorCreate) -> schemas.AuthorRetrieve:
    db_author = models.Author(**author.model_dump())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_all_authors(db: Session, skip: int = 0, limit: int = 100) -> list[schemas.AuthorRetrieve]:
    return db.query(models.Author).offset(skip).limit(limit).all()


def get_author_by_id(db: Session, author_id: int) -> schemas.AuthorRetrieve:
    return db.query(models.Author).filter(models.Author.id == author_id).first()


def get_author_by_name(db: Session, author_name: str) -> schemas.AuthorRetrieve:
    return db.query(models.Author).filter(models.Author.name == author_name).first()


def create_book(db: Session, book: schemas.BookCreate) -> schemas.BookRetrieve:
    db_book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_all_books(db: Session, skip: int = 0, limit: int = 100) -> list[schemas.BookRetrieve]:
    return db.query(models.Book).offset(skip).limit(limit).all()


def get_book_by_title(db: Session, title: str) -> schemas.BookRetrieve:
    return db.query(models.Book).filter(models.Book.title == title).first()


def get_book_by_id(db: Session, book_id: int) -> schemas.BookRetrieve:
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def filter_books_by_author(db: Session, author_id: int) -> list[schemas.BookRetrieve]:
    return db.query(models.Book).filter(models.Book.author_id == author_id).all()
