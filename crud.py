from sqlalchemy.orm import Session
import models
import schemas
from schemas import AuthorCreate


def get_all_authors(
        db: Session, skip: int | None, limit: int | None
) -> list[models.Author]:
    queryset = db.query(models.Author)
    if skip:
        queryset = queryset.offset(skip)
    if limit:
        queryset = queryset.limit(limit)
    return queryset.all()


def get_author_by_name(db: Session, name: str):
    return (
        db.query(models.Author).filter(
            models.Author.name == name
        ).first()
    )


def create_author(db: Session, author: AuthorCreate):
    db_author = models.Author(
        name=author.name,
        bio=author.bio,
    )

    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_book_list(
        skip: int | None,
        limit: int | None,
        author_id: int | None,
        db: Session
):
    queryset = db.query(models.Book)
    if author_id:
        queryset = queryset.filter(models.Book.author_id == author_id)
    if skip:
        queryset = queryset.offset(skip)
    if limit:
        queryset = queryset.limit(limit)

    return queryset.all()


def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def get_author(db: Session, author_id: int):
    return db.query(
        models.Author).filter(models.Author.id == author_id).first()


def create_book(db: Session, book: schemas.BookCreate) -> models.Book:
    db_book = models.Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book
