from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload
from typing import Optional
import models
import schemas


# Author CRUD operations
def create_author(db: Session, author: schemas.AuthorCreate) -> models.Author:
    """Create a new author in the database."""
    db_author = models.Author(name=author.name, bio=author.bio)
    db.add(db_author)
    try:
        db.commit()
        db.refresh(db_author)
    except IntegrityError as e:
        db.rollback()
        raise IntegrityError(
            "Author with this name already exists",
            params=None,
            orig=e.orig
        )
    except Exception as e:
        db.rollback()
        raise e
    return db_author


def get_authors(
        db: Session,
        skip: int = 0,
        limit: int = 10
) -> list[models.Author]:
    """Retrieve a paginated list of authors with their books eagerly loaded."""
    return db.query(models.Author).options(
        joinedload(models.Author.books)
    ).offset(skip).limit(limit).all()


def get_author_by_id(db: Session, author_id: int) -> Optional[models.Author]:
    """Retrieve a single author by ID with books eagerly loaded."""
    return db.query(models.Author).options(
        joinedload(models.Author.books)
    ).filter(models.Author.id == author_id).first()


# Book CRUD operations
def create_book(
        db: Session,
        book: schemas.BookCreate,
        author_id: int
) -> models.Book:
    """Create a new book for a specific author."""
    db_book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=author_id
    )
    db.add(db_book)
    try:
        db.commit()
        db.refresh(db_book)
    except IntegrityError as e:
        db.rollback()
        raise IntegrityError(
            "Database integrity error while creating book",
            params=None,
            orig=e.orig
        )
    except Exception as e:
        db.rollback()
        raise e
    return db_book


def get_books(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        author_id: Optional[int] = None
) -> list[models.Book]:
    """
    Retrieve a paginated list of books with author eagerly loaded.
    Optionally filter by author_id.
    """
    query = db.query(models.Book).options(
        joinedload(models.Book.author)
    )

    if author_id is not None:
        query = query.filter(models.Book.author_id == author_id)

    return query.offset(skip).limit(limit).all()


def get_books_by_author(
        db: Session,
        author_id: int,
        skip: int = 0,
        limit: int = 10
) -> list[models.Book]:
    """Retrieve books filtered by a specific
    author ID with author eagerly loaded."""
    return db.query(models.Book).options(
        joinedload(models.Book.author)
    ).filter(
        models.Book.author_id == author_id
    ).offset(skip).limit(limit).all()
