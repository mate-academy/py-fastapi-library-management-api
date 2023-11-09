from sqlalchemy.orm import Session

import models
import schemas


def get_all_authors(db: Session, skip: int, limit: int):
    return db.query(models.Author).offset(skip).limit(limit).all()


def get_single_author(db: Session, author_id: int):
    return (
        db.query(models.Author).filter(models.Author.id == author_id).first()
    )


def update_author(db: Session, author_id: int, author: schemas.AuthorCreate):
    db.query(models.Author).filter(models.Author.id == author_id).update(
        {
            models.Author.name: author.name,
            models.Author.bio: author.bio,
        }
    )
    db.commit()


def delete_author(db: Session, author_id: int):
    db.query(models.Author).filter(models.Author.id == author_id).delete()
    db.commit()


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(
        name=author.name,
        bio=author.bio,
    )

    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_all_books(db: Session, skip: int, limit: int, author_id: int = None):
    queryset = db.query(models.Book)

    if author_id is not None:
        queryset = queryset.filter(models.Book.author_id == author_id)

    return queryset.offset(skip).limit(limit).all()


def get_single_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def update_book(db: Session, book_id: int, book: schemas.BookCreate):
    db.query(models.Book).filter(models.Book.id == book_id).update(
        {
            models.Book.title: book.title,
            models.Book.summary: book.summary,
            models.Book.publication_date: book.publication_date,
            models.Book.author_id: book.author_id,
        }
    )
    db.commit()


def delete_book(db: Session, book_id: int):
    db.query(models.Book).filter(models.Book.id == book_id).delete()
    db.commit()


def create_book(db: Session, book: schemas.BookCreate):
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
