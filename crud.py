from sqlalchemy.orm import Session

import models
import schemas


def get_all_authors(db: Session) -> list[schemas.AuthorList]:
    return db.query(models.Author).all()


def get_single_author(db: Session, author_id: int) -> schemas.AuthorRetrieve:
    return db.query(models.Author).filter(models.Author.id == author_id).first()


def create_author(db: Session, author: schemas.AuthorCreate) -> schemas.AuthorRetrieve:
    db_author = models.Author(
        name=author.name,
        bio=author.bio,
    )

    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_all_books(db: Session):
    return db.query(models.Book).all()


def get_single_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def create_book(db: Session, book: schemas.BookCreate):
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
