from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

import schemas
from models import DBAuthor, DBBook


def get_authors(
        db: Session,
        skip: int | None,
        limit: int | None
):

    return (db.query(DBAuthor)
            .limit(limit)
            .offset(skip)
            .all())


def get_author(author_id: int, db: Session):
    author = db.get(DBAuthor, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


def create_author(
        db: Session,
        author_schema: schemas.AuthorCreate
):
    author_db = DBAuthor(
        name=author_schema.name,
        bio=author_schema.bio,
    )
    db.add(author_db)
    db.commit()
    db.refresh(author_db)
    return author_db


def update_author(
        author_id: int,
        author_schema: schemas.AuthorUpdate,
        db: Session,
):
    author_db = db.get(DBAuthor, author_id)
    if not author_db:
        raise HTTPException(status_code=404, detail="Author not found")
    author_db.name = author_schema.name
    author_db.bio = author_schema.bio

    db.commit()
    return author_db


def delete_author(
        author_id: int,
        db: Session
):
    author = db.get(DBAuthor, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    db.delete(author)
    db.commit()
    return {"ok": True}


def get_books(
        db: Session,
        author_id: int | None,
        skip: int | None,
        limit: int | None
):
    if author_id:
        return (
            db.execute(
                select(DBBook)
                .limit(limit)
                .offset(skip)
                .where(DBBook.author_id == author_id)
            ).scalars().all()
        )
    return (db.query(DBBook).
            limit(limit).
            offset(skip).all())


def create_book(
        db: Session,
        book_schema: schemas.BookCreate
):
    db_book = DBBook(
        title=book_schema.title,
        summary=book_schema.summary,
        publication_date=book_schema.publication_date,
        author_id=book_schema.author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_book(book_id, db):
    book_db = db.get(DBBook, book_id)
    if not book_db:
        raise HTTPException(status_code=404, detail="Book not found")
    return book_db


def update_book(book_id, book_schema, db):
    book_db = db.get(DBBook, book_id)
    if not book_db:
        raise HTTPException(status_code=404, detail="Book not found")
    book_db.title = book_schema.title
    book_db.summary = book_schema.summary
    book_db.publication_date = book_schema.publication_date
    book_db.author_id = book_schema.author_id
    db.commit()
    db.refresh(book_db)
    return book_db


def delete_book(book_id, db):
    book_db = db.get(DBBook, book_id)
    if not book_db:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book_db)
    db.commit()
    return {"ok": True}
