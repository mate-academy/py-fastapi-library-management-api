from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models import Author, Book
from schemas import (
    AuthorCreateUpdateDto,
    BookCreateUpdateDto,
)


def get_authors(
    db: Session,
    skip: int = 0,
    limit: int = 10
) -> list[Author]:
    return db.execute(select(Author).offset(skip).limit(limit)).scalars().all()


def get_author_by_id(
    id: int,
    db: Session
) -> Author:
    author = db.execute(select(Author).where(Author.id == id)).scalar_one_or_none()

    if author is None:
        raise HTTPException(
            detail=f"Author with this id {id} doesn't exist.",
            status_code=404
        )
    return author


def create_author(
    author: AuthorCreateUpdateDto,
    db: Session
) -> Author:
    try:
        author_model = Author(
            name=author.name,
            bio=author.bio
        )
        db.add(author_model)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Author with this name {author.name} already exists"
        )

    db.refresh(author_model)
    return author_model


def update_author(
    id: int,
    author: AuthorCreateUpdateDto,
    db: Session
) -> Author:
    author_model = get_author_by_id(
        id=id,
        db=db
    )

    try:
        author_model.name = author.name
        author_model.bio = author.bio

        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            detail=f"Author with this name {author.name} already exists",
            status_code=400
        )
    except AttributeError:
        db.rollback()
        raise HTTPException(
            detail=f"Wrong data.",
            status_code=400
        )

    db.refresh(author_model)
    return author_model


def delete_author(
    id: int,
    db: Session
) -> None:
    author = get_author_by_id(
        id=id,
        db=db
    )
    
    db.delete(author)
    db.commit()


def get_books(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    author_id: int | None = None
) -> list[Book]:
    query = select(Book).offset(skip).limit(limit)
    if author_id is not None:
        query = query.where(Book.author_id == author_id)
    return db.execute(query).scalars().all()


def get_book_by_id(
    id: int,
    db: Session
) -> Book:
    book = db.execute(select(Book).where(Book.id == id)).scalar_one_or_none()

    if book is None:
        raise HTTPException(
            detail=f"Book with this id {id} doesn't exist.",
            status_code=404
        )
    return book


def create_book(
    book: BookCreateUpdateDto,
    db: Session
) -> Book:
    author_model = get_author_by_id(
        id=book.author_id,
        db=db
    )
    book_model = Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author=author_model
    )
    
    db.add(book_model)
    db.commit()
    db.refresh(book_model)
    return book_model


def update_book(
    id: int,
    book: BookCreateUpdateDto,
    db: Session
) -> Book:
    book_model = get_book_by_id(
        id=id,
        db=db
    )
    author_model = get_author_by_id(
        id=book.author_id,
        db=db
    )
    try:
        book_model.title = book.title
        book_model.summary = book.summary
        book_model.publication_date = book.publication_date
        book_model.author = author_model

        db.commit()
    except AttributeError:
        db.rollback()
        raise HTTPException(
            detail=f"Wrong data.",
            status_code=400
        )

    db.refresh(book_model)
    return book_model


def delete_book(
    id: int,
    db: Session
) -> None:
    book = get_book_by_id(
        id=id,
        db=db
    )
    
    db.delete(book)
    db.commit()
