import models
import schemas

from sqlalchemy.orm import Session, Query


def get_authors(
    db: Session, skip: int = 0, limit: int = 10
) -> Query[models.DBAuthor]:
    return db.query(models.DBAuthor).offset(skip).limit(limit).all()


def get_author(db: Session, author_id: int) -> models.DBAuthor:
    return (
        db.query(models.DBAuthor)
        .filter(models.DBAuthor.id == author_id)
        .first()
    )


def get_author_by_name(db: Session, name: str) -> models.DBAuthor:
    return (
        db.query(models.DBAuthor)
        .all()
        .filter(models.DBAuthor.name == name)
        .first()
    )


def create_author(
    db: Session, author: schemas.AuthorCreate
) -> models.DBAuthor:
    db_author = models.DBAuthor(name=author.name, bio=author.bio)

    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_books(
    db: Session,
    author_id: int | None = None,
) -> Query[models.DBBook]:
    queryset = db.query(models.DBBook)

    if author_id is not None:
        queryset = queryset.filter(models.DBBook.author_id == author_id)

    return queryset.all()


def create_book(db: Session, book: schemas.BookCreate) -> models.DBBook:
    db_book = models.DBAuthor(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id,
    )

    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book
