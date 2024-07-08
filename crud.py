from sqlalchemy.orm import Session

import models, schemas


def get_authors(db: Session) -> list[models.Author]:
    return db.query(models.Author).all()


def get_author_by_id(db: Session, author_id: int) -> models.Author:
    return db.query(models.Author).filter(models.Author.id == author_id).first()


def get_author_by_name(db: Session, author_name: str) -> models.Author:
    return db.query(models.Author).filter(models.Author.name == author_name).first()


def create_author(db: Session, author: schemas.AuthorCreate) -> models.Author:
    db_author = models.Author(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_books_list(
        db: Session,
        author_id: int | None = None,
) -> list[models.Book]:
    queryset = db.query(models.Book)

    if author_id is not None:
        queryset = queryset.filter(models.Book.author_id == author_id)

    return queryset.all()


def create_book_for_author(
        db: Session,
        author_id: int,
        book: schemas.BookCreate
) -> models.Book:
    db_book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=author_id,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
