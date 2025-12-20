from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
import database
import schemas


def create_new_author(db: Session, author: schemas.AuthorCreateSchema):
    author = database.Author(
        name=author.name,
        bio=author.bio
    )
    db.add(author)
    db.commit()
    db.refresh(author)

    return author


def get_all_authors_with_pagination(db: Session, skip: int = 0, limit: int = 10):
    return (
        db.query(database.Author)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_all_books_with_pagination(db: Session, skip: int = 0, limit: int = 10):
    return (
        db.query(database.Book)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_author_by_id(db: Session, author_id: int):
    author = db.query(database.Author).filter(database.Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


def add_book_by_author_id(db: Session, author_id: int, book: database.Book):
    author = db.get(database.Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    book = database.Book(title=book.title,
                         summary=book.summary,
                         publication_date=book.publication_date,
                         author_id=author_id)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def get_book_by_author_id(db: Session, author_id: int):
    author = db.query(database.Author).filter(database.Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return db.query(database.Book).filter(database.Book.author_id == author.id).all()
