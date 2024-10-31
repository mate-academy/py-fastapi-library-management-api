from sqlalchemy.orm import Session

import models, schemas


def get_all_books(
    db: Session,
    author_id: int | None = None,
    skip: int = 0, limit: int = 10
):
    queryset = db.query(models.DBBook)
    if author_id:
        queryset = queryset.filter(models.DBBook.author_id == author_id)
    return queryset.offset(skip).limit(limit).all()


def get_book(db: Session, book_id: int):
    return db.query(models.DBBook).filter(models.DBBook.id == book_id).first()

def get_book_by_author_id(db: Session, author_id: int):
    return db.query(models.DBBook).filter(models.DBBook.author_id == author_id).all()


def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.DBBook(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id,
    )

    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return book


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.DBAuthor(
        name=author.name,
        bio=author.bio,
    )

    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return author


def get_all_authors(db: Session):
    return db.query(models.DBAuthor).all()


def get_author(db: Session, author_id: int):
    return db.query(models.DBAuthor).filter(models.DBAuthor.id == author_id).first()