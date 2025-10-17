from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

# use absolute imports to avoid "attempted relative import with no known parent package"
import models
import schemas


def get_author(db: Session, author_id: int) -> Optional[models.AuthorModel]:
    return db.get(models.AuthorModel, author_id)


def get_author_by_name(db: Session, name: str) -> Optional[models.AuthorModel]:
    return db.query(models.AuthorModel).filter(models.AuthorModel.name == name).first()


def get_authors(db: Session, skip: int = 0, limit: int = 100) -> List[models.AuthorModel]:
    return db.query(models.AuthorModel).offset(skip).limit(limit).all()


def create_author(db: Session, author: schemas.AuthorCreate) -> models.AuthorModel:
    db_author = models.AuthorModel(**author.dict())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def update_author(db: Session, author_id: int, author_update: schemas.AuthorUpdate) -> Optional[models.AuthorModel]:
    db_author = get_author(db, author_id)
    if not db_author:
        return None
    update_data = author_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_author, key, value)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def delete_author(db: Session, author_id: int) -> Optional[models.AuthorModel]:
    db_author = get_author(db, author_id)
    if not db_author:
        return None
    db.delete(db_author)
    db.commit()
    return db_author


def get_book(db: Session, book_id: int) -> Optional[models.BookModel]:
    return db.get(models.BookModel, book_id)


def get_books(db: Session, skip: int = 0, limit: int = 100, author_id: Optional[int] = None) -> List[models.BookModel]:
    q = db.query(models.BookModel)
    if author_id is not None:
        q = q.filter(models.BookModel.author_id == author_id)
    return q.offset(skip).limit(limit).all()


def create_book(db: Session, book: schemas.BookCreate) -> models.BookModel:
    # pre-validate author to give clear error instead of DB integrity error
    if db.get(models.AuthorModel, book.author_id) is None:
        raise ValueError("Author not found")

    db_book = models.BookModel(**book.dict())
    db.add(db_book)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
    db.refresh(db_book)
    return db_book


def update_book(db: Session, book_id: int, book_update: schemas.BookUpdate) -> Optional[models.BookModel]:
    db_book = get_book(db, book_id)
    if not db_book:
        return None
    update_data = book_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_book, key, value)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int) -> Optional[models.BookModel]:
    db_book = get_book(db, book_id)
    if not db_book:
        return None
    db.delete(db_book)
    db.commit()
    return db_book

