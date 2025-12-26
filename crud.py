from sqlalchemy.orm import Session
import schemas
import models


# ---------- AUTHOR CRUD
def create_author(db: Session, author_data: schemas.AuthorCreate):
    author = models.DBAuthor(
        name=author_data.name,
        bio=author_data.bio,
    )
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


def get_authors(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.DBAuthor).offset(skip).limit(limit).all()


def get_author_by_id(db: Session, author_id: int):
    return db.query(models.DBAuthor).filter(models.DBAuthor.id == author_id).first()


# ---------- BOOK CRUD
def create_book(
    db: Session,
    author_id: int,
    book_data: schemas.BookCreate
) -> models.DBBook:
    book = models.DBBook(
        title=book_data.title,
        summary=book_data.summary,
        publication_date=book_data.publication_date,
        author_id=author_id,
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def get_books(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.DBBook).offset(skip).limit(limit).all()


def get_books_by_author(
    db: Session,
    author_id: int,
    skip: int = 0,
    limit: int = 10
):
    return (
        db.query(models.DBBook)
        .filter(models.DBBook.author_id == author_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
