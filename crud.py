from sqlalchemy.orm import Session
import models
import schemas


def get_all_author(
        db: Session,
        skip: int = 0,
        limit: int = 10
) -> list[models.Author]:

    return db.query(models.Author).offset(skip).limit(limit).all()


def create_author(db: Session, author: schemas.AuthorCreate) -> models.Author:
    db_author = models.Author(
        name=author.name,
        bio=author.bio,
    )

    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_author(db: Session, author_id: int) -> models.Author:
    return db.query(
        models.Author
    ).filter(models.Author.id == author_id).first()


def get_author_by_name(db: Session, name: str) -> models.Author:
    return db.query(models.Author).filter(models.Author.name == name).first()


def get_all_book(
        db: Session,
        author_id: int | None = None,
        skip: int = 0,
        limit: int = 10
) -> list[models.Book]:

    db_book = db.query(models.Book)
    if author_id is not None:
        db_book = db_book.filter(models.Book.author_id == author_id)
    db_book = db_book.offset(skip).limit(limit)
    return db_book.all()


def create_book(db: Session, book: schemas.BookCreate) -> models.Book:
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
