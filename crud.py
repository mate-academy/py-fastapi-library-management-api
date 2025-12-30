from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc
from typing import List, Optional
import models
import schemas


# Author CRUD operations
def create_author(db: Session, author: schemas.AuthorCreate) -> models.Author:
    """Create a new author"""
    db_author = models.Author(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_authors(db: Session, skip: int = 0, limit: int = 100) -> List[models.Author]:
    """Get list of authors with pagination"""
    return db.query(models.Author).offset(skip).limit(limit).all()


def get_author(db: Session, author_id: int) -> Optional[models.Author]:
    """Get a single author by ID"""
    return db.query(models.Author).filter(models.Author.id == author_id).first()


def update_author(db: Session, author_id: int, author_update: schemas.AuthorUpdate) -> Optional[models.Author]:
    """Update an existing author"""
    db_author = get_author(db, author_id)
    if db_author:
        update_data = author_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_author, key, value)
        db.commit()
        db.refresh(db_author)
    return db_author


def delete_author(db: Session, author_id: int) -> Optional[models.Author]:
    """Delete an author"""
    db_author = get_author(db, author_id)
    if db_author:
        db.delete(db_author)
        db.commit()
    return db_author


# Book CRUD operations
def create_book(db: Session, book: schemas.BookCreate) -> models.Book:
    """Create a new book"""
    db_book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_books(db: Session, skip: int = 0, limit: int = 100, author_id: Optional[int] = None) -> List[models.Book]:
    """Get list of books with pagination and optional author filter"""
    query = db.query(models.Book)
    if author_id is not None:
        query = query.filter(models.Book.author_id == author_id)
    return query.order_by(desc(models.Book.publication_date)).offset(skip).limit(limit).all()


def get_book(db: Session, book_id: int) -> Optional[models.Book]:
    """Get a single book by ID"""
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def update_book(db: Session, book_id: int, book_update: schemas.BookUpdate) -> Optional[models.Book]:
    """Update an existing book"""
    db_book = get_book(db, book_id)
    if db_book:
        update_data = book_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_book, key, value)
        db.commit()
        db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int) -> Optional[models.Book]:
    """Delete a book"""
    db_book = get_book(db, book_id)
    if db_book:
        db.delete(db_book)
        db.commit()
    return db_book


def get_books_by_author(db: Session, author_id: int) -> List[models.Book]:
    """Get all books by a specific author"""
    return db.query(models.Book).filter(models.Book.author_id == author_id).all()


# NEW: Get books with author info (eager loading)
def get_books_with_authors(
        db: Session, skip: int = 0, limit: int = 100, author_id: Optional[int] = None
) -> List[models.Book]:
    """Get list of books with author information"""
    query = db.query(models.Book).options(joinedload(models.Book.author))

    if author_id is not None:
        query = query.filter(models.Book.author_id == author_id)

    return query.order_by(desc(models.Book.publication_date)).offset(skip).limit(limit).all()
