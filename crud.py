from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import HTTPException
from db.models import Author, Book
from schemas import AuthorCreate, BookCreate


def get_all_authors(db: Session) -> list[Author]:
    try:
        return db.query(Author).all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database query failed")


def get_authors_with_pagination(
        db: Session,
        skip: int = 0,
        limit: int = 10
) -> list[Author]:
    try:
        return db.query(Author).offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database query failed")


def get_author_by_name(db: Session, name: str) -> Author | None:
    try:
        return db.query(Author).filter(Author.name == name).first()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database query failed")


def get_author_by_id(db: Session, author_id: int) -> Author | None:
    try:
        return db.query(Author).filter(Author.id == author_id).first()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database query failed")


def create_author(db: Session, author: AuthorCreate) -> Author:
    try:
        db_author = Author(
            name=author.name,
            bio=author.bio
        )
        db.add(db_author)
        db.commit()
        db.refresh(db_author)
        return db_author
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Author creation failed due to integrity issues")
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database operation failed")


def get_all_books(db: Session, author_id: int | None = None) -> list[Book]:
    try:
        queryset = db.query(Book)
        if author_id:
            queryset = queryset.filter(Book.author_id == author_id)
        return queryset.all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database query failed")


def get_books_with_pagination(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        author_id: int | None = None
) -> list[Book]:
    try:
        query = db.query(Book)
        if author_id:
            query = query.filter(Book.author_id == author_id)
        return query.offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database query failed")


def create_book(db: Session, book: BookCreate) -> Book:
    try:
        db_book = Book(
            title=book.title,
            summary=book.summary,
            publication_date=book.publication_date,
            author_id=book.author_id
        )
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return db_book
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Book creation failed due to integrity issues")
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database operation failed")
