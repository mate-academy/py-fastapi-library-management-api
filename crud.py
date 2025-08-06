from sqlalchemy.orm import Session

import models
import schemas


def get_all_authors(db: Session, skip: int, limit: int):
    return (db
            .query(models.Author)
            .offset(skip)
            .limit(limit)
            .all()
            )


def get_author_by_name(db: Session, name: str):
    return (db
            .query(models.Author)
            .filter(models.Author.name == name)
            .first()
            )


def get_author_by_id(db: Session, author_id: int):
    return (db
            .query(models.Author)
            .filter(models.Author.id == author_id)
            .first()
            )


def create_author(db: Session, author: schemas.AuthorCreate):
    author_db = models.Author(
        name=author.name,
        bio=author.bio
    )

    db.add(author_db)
    db.commit()
    db.refresh(author_db)

    return author_db


def get_all_books(db: Session, skip: int, limit: int):
    return (db
            .query(models.Book)
            .offset(skip)
            .limit(limit)
            .all()
            )


def get_all_books_by_author_id(db: Session, author_id: int):
    return (db
            .query(models.Book)
            .filter(models.Book.author_id == author_id)
            .all()
            )


def create_book(db: Session, book: schemas.BookCreate):
    book_db = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id
    )

    db.add(book_db)
    db.commit()
    db.refresh(book_db)

    return book_db
