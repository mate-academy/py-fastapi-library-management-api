from sqlalchemy import desc
from sqlalchemy.orm import joinedload, Session

import models
import schemas


def get_author_by_name(db: Session, name: str) -> models.Author:
    return db.query(models.Author).filter(models.Author.name == name).first()


def create_author(db: Session, author: schemas.AuthorCreate) -> models.Author:
    db_author = models.Author(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_authors(
    db: Session,
    name: str = None,
    sort_by: str = None,
    sort_order: str = "asc",
    skip: int = 0,
    limit: int = 5,
) -> list[models.Author]:
    query = db.query(models.Author)
    if name:
        query = query.filter(models.Author.name.ilike(f"%{name}%"))

    if sort_by:
        if sort_order == "desc":
            query = query.order_by(desc(sort_by))
        else:
            query = query.order_by(sort_by)

    return query.offset(skip).limit(limit).all()


def get_author(db: Session, author_id: int) -> models.Author:
    return (
        db.query(models.Author)
        .options(joinedload(models.Author.books))
        .filter(models.Author.id == author_id)
        .first()
    )


def update_author(
    db: Session, author_id: int, author: schemas.AuthorUpdate
) -> models.Author:
    db_author = db.query(models.Author).filter(models.Author.id == author_id).first()
    db_author.name = author.name
    db_author.bio = author.bio
    db.commit()
    db.refresh(db_author)
    return db_author


def delete_author(db: Session, author_id: int) -> None:
    db.query(models.Book).filter(models.Book.author_id == author_id).delete()
    db.query(models.Author).filter(models.Author.id == author_id).delete()
    db.commit()


def create_book(db: Session, book: schemas.BookCreate, author_id: int) -> models.Book:
    db_book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=author_id,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def update_book(db: Session, book_id: int, book: schemas.BookUpdate) -> models.Book:
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    db_book.title = book.title
    db_book.summary = book.summary
    db_book.publication_date = book.publication_date
    db.commit()
    db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int) -> None:
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    db.delete(db_book)
    db.commit()


def get_books(
    db: Session,
    title: str = None,
    sort_by: str = None,
    sort_order: str = "asc",
    skip: int = 0,
    limit: int = 5,
) -> list[models.Book]:
    query = db.query(models.Book)
    if title:
        query = query.filter(models.Book.title.ilike(f"%{title}%"))

    if sort_by:
        if sort_order == "desc":
            query = query.order_by(desc(sort_by))
        else:
            query = query.order_by(sort_by)

    return query.offset(skip).limit(limit).all()


def get_book(db: Session, book_id: int) -> models.Book:
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def get_books_by_author(
    db: Session, author_id: int, skip: int = 0, limit: int = 5
) -> list[models.Book]:
    return (
        db.query(models.Book)
        .filter(models.Book.author_id == author_id)
        .order_by(models.Book.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
