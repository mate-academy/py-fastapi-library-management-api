from sqlalchemy.orm import Session

import models
import schemas


def get_author_list(db: Session, skip: int = 0, limit: int = 5):
    return db.query(models.Author).offset(skip).limit(limit).all()


def get_author_by_id(db: Session, author_id: int):
    return db.query(models.Author).filter(
        models.Author.id == author_id
    ).first()


def create_author(db: Session, author: schemas.AuthorCreate):
    author = models.Author(name=author.name, bio=author.bio)

    db.add(author)
    db.commit()
    db.refresh(author)

    return author


def get_book_list(db: Session, skip: int = 0, limit: int = 5):
    return db.query(models.Book).offset(skip).limit(limit).all()


def filter_book_by_author_id(db: Session, author_id: int):
    return db.query(models.Book).filter(models.Book.author_id == author_id)


def create_book(db: Session, book: schemas.BookCreate):
    book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id,
    )

    db.add(book)
    db.commit()
    db.refresh(book)

    return book
