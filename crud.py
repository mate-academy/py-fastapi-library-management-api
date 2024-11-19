from fastapi import HTTPException
from sqlalchemy.orm import Session

import models
import schemas


def get_author_by_name(db: Session, name: str):
    return (db.query(models.DBAuthor)
            .filter(models.DBAuthor.name == name).first())


def create_author(db: Session, author: schemas.AuthorCreate):
    if get_author_by_name(db, author.name):
        raise HTTPException(
            status_code=400, detail="Author with this name already exists"
        )

    db_author = models.DBAuthor(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_author_list(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.DBAuthor).offset(skip).limit(limit).all()


def get_author_by_id(db: Session, author_id: int):
    author = (
        db.query(models.DBAuthor).filter(models.DBAuthor.id == author_id)
        .first())
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


def update_author(db: Session, author_id: int, author: schemas.AuthorUpdate):
    db_author = get_author_by_id(db, author_id)
    if author.name:
        db_author.name = author.name
    if author.bio:
        db_author.bio = author.bio
    db.commit()
    db.refresh(db_author)
    return db_author


def delete_author(db: Session, author_id: int):
    db_author = get_author_by_id(db, author_id)
    if db_author:
        db.delete(db_author)
        db.commit()
        return {"message": f"Author {db_author.name} successfully deleted"}


def get_book_by_author_and_title(db: Session, author_id: int, title: str):
    return (
        db.query(models.DBBook)
        .filter(models.DBBook.author_id == author_id)
        .filter(models.DBBook.title == title)
        .first()
    )


def create_book(db: Session, book: schemas.BookCreate):
    if get_book_by_author_and_title(db, book.author_id, book.title):
        raise HTTPException(
            status_code=400,
            detail="Book with this title and author already exists"
        )

    db_book = models.DBBook(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_book_list(
        db: Session,
        author_id: int | None = None,
        skip: int = 0,
        limit: int = 10
):
    query = db.query(models.DBBook)
    if author_id is not None:
        query = query.filter(models.DBBook.author_id == author_id)
    return query.offset(skip).limit(limit).all()


def get_book_by_id(db: Session, book_id: int):
    book = db.query(models.DBBook).filter(models.DBBook.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


def update_book(db: Session, book_id: int, book: schemas.BookUpdate):
    db_book = get_book_by_id(db, book_id)
    if book.title:
        db_book.title = book.title
    if book.summary:
        db_book.summary = book.summary
    if book.publication_date:
        db_book.publication_date = book.publication_date
    if book.author_id:
        db_book.author_id = book.author_id
    db.commit()
    db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int):
    db_book = get_book_by_id(db, book_id)
    if db_book:
        db.delete(db_book)
        db.commit()
        return {"message": f"Book with id {book_id} successfully deleted"}
