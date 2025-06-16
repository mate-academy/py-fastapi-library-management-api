from sqlalchemy.orm import Session
from sqlalchemy import exc

import models
import schemas


def get_all_books(
        db: Session,
        author_id: int = None,
        skip: int = 0,
        limit: int = 100,
):
    if author_id:
        return db.query(models.DBBook).filter(
            models.DBBook.author_id == author_id).offset(skip).limit(limit).all()
    return db.query(models.DBBook).offset(skip).limit(limit).all()


def create_book_for_author(db: Session, book_data: schemas.BookCreate):

    author_exists = db.query(models.DBAuthor).filter(
        models.DBAuthor.id == book_data.author_id
    ).first()

    if not author_exists:
        raise ValueError(f"Автор з ID '{book_data.author_id}' не існує.")

    new_book = models.DBBook(
        title=book_data.title,
        summary=book_data.summary,
        publication_date=book_data.publication_date,
        author_id=book_data.author_id,
    )
    try:
        db.add(new_book)
        db.commit()
        db.refresh(new_book)
    except exc.IntegrityError:
        db.rollback()
        raise ValueError("Помилка цілісності даних при створенні книги.")
    except Exception as e:
        db.rollback()
        raise Exception(f"Несподівана помилка при створенні книги: {e}")

    return new_book


def create_author(db: Session, author_data: schemas.AuthorCreate):

    author_existing = db.query(models.DBAuthor).filter(
        models.DBAuthor.name == author_data.name).first()

    if author_existing:
        raise ValueError(f"Автор з іменем '{author_data.name}' вже існує.")

    new_author = models.DBAuthor(
        name=author_data.name,
        bio=author_data.bio
    )
    try:
        db.add(new_author)
        db.commit()
        db.refresh(new_author)
    except exc.IntegrityError:
        db.rollback()
        raise ValueError("Помилка цілісності даних при створенні автора.")
    except Exception as e:
        db.rollback()
        raise Exception(f"Несподівана помилка при створенні автора: {e}")


def get_all_authors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.DBAuthor).offset(skip).limit(limit).all()


def get_author_by_id(db: Session, author_id: int):
    return db.query(models.DBAuthor).filter(models.DBAuthor.id == author_id).first()
