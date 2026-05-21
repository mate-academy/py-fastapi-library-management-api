from sqlalchemy.orm import Session
import models
from fastapi import HTTPException
import schemas


def get_book_by_id(book_id: int, db: Session):
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def get_book_by_title(title: str, db: Session):
    return db.query(models.Book).filter(models.Book.title == title).first()


def create_book(author_id: int, book: schemas.BookCreate, db: Session):
    if not get_author_by_id(author_id, db):
        raise HTTPException(status_code=404, detail="Author not found")
    db_book = models.Book(**book.model_dump(), author_id=author_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_author_by_id(author_id: int, db: Session):
    return db.query(models.Author).filter(models.Author.id == author_id).first()


def get_author_by_name(name: str, db: Session):
    return db.query(models.Author).filter(models.Author.name == name).first()


def create_author(author: schemas.AuthorCreate, db: Session):
    if get_author_by_name(author.name, db):
        raise HTTPException(
            status_code=400, detail="Author with this name already exists"
        )
    db_author = models.Author(**author.model_dump())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_all_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()


def get_books_by_author(author_id: int, db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Book)
        .filter(models.Book.author_id == author_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_all_authors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Author).offset(skip).limit(limit).all()


def get_authors_with_books(db: Session):
    return db.query(models.Author).filter(models.Author.books.any()).all()


def delete_book(book_id: int, db: Session):
    book = get_book_by_id(book_id, db)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"detail": "Book deleted"}


def delete_author(author_id: int, db: Session):
    author = get_author_by_id(author_id, db)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    db.delete(author)
    db.commit()
    return {"detail": "Author deleted"}
