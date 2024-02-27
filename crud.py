from sqlalchemy.orm import Session

from db import models
import schemas


def get_author_by_id(db: Session, author_id: int):
    return db.query(models.DBAuthor).filter(models.DBAuthor.id == author_id).first()


def get_author_by_name(db: Session, author_name: str):
    return db.query(models.DBAuthor).filter(models.DBAuthor.name == author_name).first()


def get_all_authors(db: Session):
    return db.query(models.DBAuthor).all()


def get_authors_with_skip_limit(db: Session, skip_value: int, limit_value: int):
    output_list = db.query(models.DBAuthor).all()
    return output_list[skip_value:limit_value]


def create_author(db: Session, new_author: schemas.AuthorCreate):
    db_author = models.DBAuthor(
        name=new_author.name,
        bio=new_author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_book_by_title(db: Session, book_title: str):
    return db.query(models.DBBook).filter(models.DBBook.title == book_title).first()


def get_all_books(db: Session):
    return db.query(models.DBBook).all()


def get_books_by_author_id(author_id: int, db:Session):
    return db.query(models.DBBook).filter(models.DBBook.author_id == author_id)


def get_books_with_skip_limit(skip_value: int, limit_value: int, db: Session):
    output_list = db.query(models.DBBook).all()
    return output_list[skip_value:limit_value]


def create_book(db: Session, new_book: schemas.BookCreate):
    db_book = models.DBBook(
        title=new_book.title,
        summary=new_book.summary,
        publication_date=new_book.publication_date,
        author_id=new_book.author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
