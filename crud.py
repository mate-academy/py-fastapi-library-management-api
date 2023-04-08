from sqlalchemy.orm import Session

from library import models
import schemas


def get_all_books(db: Session):
    return db.query(models.Book).all()


def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,

    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book


def get_author(library: Session, author_id: int):
    return library.query(models.Author).filter(
        models.Author.id == author_id
    ).first()


def get_all_authors(library: Session):
    return library.query(models.Author).all()


def create_author(library: Session, author: schemas.AuthorCreate):
    library_author = models.Author(
        name=author.name,
        bio=author.bio,
    )
    library.add(library_author)
    library.commit()
    library.refresh(library_author)

    return library_author



