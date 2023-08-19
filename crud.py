from sqlalchemy.orm import Session

import models
import schemas

# ⬇️ --- AUTHORS CRUD --- ⬇️


def create_author(db: Session, author: schemas.AuthorCreateUpdate) -> models.Author:
    db_author = models.Author(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_authors(db: Session, page: int = 0, page_size: int = 100) -> list[models.Author]:
    return db.query(models.Author).offset(page).limit(page_size).all()


def get_detailed_author(db: Session, author_id: int) -> models.Author | None:
    return db.query(models.Author).filter(models.Author.id == author_id).first()


def get_author_by_name(db: Session, author_name: str) -> models.Author | None:
    return db.query(models.Author).filter(models.Author.name == author_name).first()


def update_author(
    db: Session,
    author_id_to_update: int,
    author_update_data: schemas.AuthorCreateUpdate,
) -> models.Author | None:
    db_author = get_detailed_author(db=db, author_id=author_id_to_update)
    if db_author is not None:
        for key, value in author_update_data.model_dump().items():
            setattr(db_author, key, value)
        db.commit()
        db.refresh(db_author)
    return db_author


def delete_author(db: Session, author_id_to_delete: int) -> models.Author | None:
    db_author = get_detailed_author(db=db, author_id=author_id_to_delete)
    if db_author is not None:
        db.delete(db_author)
        db.commit()
    return db_author


# ⬇️ --- BOOKS CRUD --- ⬇️


def create_book(db: Session, book_to_create: schemas.BookCreateUpdate) -> models.Book:
    db_book = models.Book(**book_to_create.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_books(db: Session, page: int = 0, page_size: int = 100) -> list[models.Book]:
    return db.query(models.Book).offset(page).limit(page_size).all()


def get_detailed_book(db: Session, book_id: int) -> models.Book | None:
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def update_book(
    db: Session, book_id_to_update: int, book_update_data: schemas.BookCreateUpdate
) -> models.Book | None:
    db_book = get_detailed_book(db=db, book_id=book_id_to_update)

    if db_book is not None:
        for key, value in book_update_data.model_dump().items():
            setattr(db_book, key, value)
        db.commit()
        db.refresh(db_book)
    return db_book


def get_book_by_title(db: Session, book_title: str) -> models.Book | None:
    return db.query(models.Book).filter(models.Book.title == book_title).first()


def delete_book(db: Session, book_id: int) -> models.Book | None:
    db_book = get_detailed_book(db=db, book_id=book_id)
    if db_book is not None:
        db.delete(db_book)
        db.commit()
    return db_book
