from sqlalchemy.orm import Session

import models
import schemas


def get_author_list(db: Session) -> list[models.Author]:
    return db.query(models.Author).all()


def get_author_by_id(db: Session, pk: int) -> models.Author | None:
    return db.query(models.Author).get(ident=pk)


def create_author(db: Session, data: schemas.AuthorCreateModel) -> models.Author:
    author = models.Author(**data.model_dump())

    db.add(author)
    db.commit()
    db.refresh(author)
    return author


def get_book_list(
    db: Session,
    author_id: int | None = None
) -> list[models.Book]:
    query = db.query(models.Book)

    if author_id is not None:
        query = query.filter(models.Book.author_id == author_id)

    return query.all()


def create_book(db: Session, data: schemas.BookCreateModel) -> models.Book:
    book = models.Book(**data.model_dump())

    db.add(book)
    db.commit()
    db.refresh(book)

    return book
