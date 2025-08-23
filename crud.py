from sqlalchemy.orm import Session

import models
import schemas


def get_all_authors(
        skip: int,
        limit: int,
        db: Session
) -> list[models.AuthorModel]:
    return db.query(models.AuthorModel).offset(skip).limit(limit).all()


def create_author(
        db: Session,
        author_schema: schemas.AuthorCreateSchema
) -> models.AuthorModel:
    author = models.AuthorModel(
        name=author_schema.name,
        bio=author_schema.bio
    )
    db.add(author)
    db.commit()
    db.refresh(author)

    return author


def get_author(db: Session, author_id: int) -> models.AuthorModel:
    return db.query(models.AuthorModel).get(author_id)


def get_author_by_name(db: Session, name: str) -> models.AuthorModel:
    return db.query(models.AuthorModel).filter(models.AuthorModel.name == name).first()


def get_all_books(
        skip: int,
        limit: int,
        db: Session,
        author_id: int | None = None
) -> list[models.BookModel]:
    queryset = db.query(models.BookModel).offset(skip).limit(limit)
    if author_id:
        queryset = queryset.filter(models.BookModel.author_id == author_id)
    return queryset.all()


def get_book(db: Session, book_id: int) -> models.BookModel:
    return db.query(models.BookModel).get(book_id)


def create_book(
        author_id: int,
        book_schema: schemas.BookCreateSchema,
        db: Session
) -> models.BookModel:
    book = models.BookModel(
        title=book_schema.title,
        summary=book_schema.summary,
        publication_date=book_schema.publication_date,
        author_id=author_id
    )
    db.add(book)
    db.commit()
    db.refresh(book)

    return book
