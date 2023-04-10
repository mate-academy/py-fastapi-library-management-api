from sqlalchemy.orm import Session

import models
import schemas


def create_author(author: schemas.AuthorCreate, db: Session) -> models.Author:
    new_author = models.Author(
        name=author.name,
        bio=author.bio,
    )
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author


def get_author_list(skip: int, limit: int, db: Session) -> list[models.Author]:
    return db.query(models.Author).all()[skip:limit]


def get_single_author(author_id: int, db: Session) -> models.Author:
    return db.query(models.Author).filter(models.Author.id == author_id).first()


def get_book_list(skip: int, limit: int, db: Session, author_id: int | None = None) -> list[models.Book]:
    queryset = db.query(models.Book)

    if author_id is not None:
        queryset = queryset.filter(models.Book.author.has(id=author_id))

    return queryset.all()[skip:limit]


def create_book(db: Session, book: schemas.BookCreate, author_id: int) -> models.Book:
    new_book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=author_id
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

