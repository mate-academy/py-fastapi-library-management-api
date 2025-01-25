from sqlalchemy.orm import Session

from src import models, schemas


def get_all_authors(db: Session):
    return db.query(models.Author).all()


def create_author(db: Session, author: schemas.AuthorCreateResponseSchema):
    db_author = models.Author(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_author_by_name(db: Session, name: str):
    return db.query(models.Author).filter(models.Author.name == name).first()


def get_all_books(db: Session):
    return db.query(models.Book).all()


def create_book(db: Session, book: schemas.BookCreateResponseSchema):
    db_book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book

def get_book_by_title(db: Session, title: str):
    return db.query(models.Book).filter(models.Book.title == title).first()
