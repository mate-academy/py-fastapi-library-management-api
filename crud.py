from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import select, Sequence
from sqlalchemy.orm import Session


import models
import schemas


def update_function(
        obj,
        data: BaseModel,
        exclude: set,
        exclude_unset: bool = False
):
    for field, value in data.model_dump(
            exclude_unset=exclude_unset, exclude=exclude
    ).items():
        setattr(obj, field, value)

    return obj


def get_all_authors(
        db: Session,
        skip: int = 0,
        limit: int = 10
) -> Sequence[models.DBAuthor]:
    return db.scalars(select(models.DBAuthor).offset(skip).limit(limit)).all()


def get_author_by_id(
        db: Session,
        author_id: int
):
    return db.scalar(
        select(models.DBAuthor).where(models.DBAuthor.id == author_id)
    )


def create_author(
        db: Session,
        author_info: schemas.AuthorCreate
):
    db_books = author_info.books
    author_info = author_info.model_dump(exclude={"books"})

    try:
        if db.scalar(select(models.DBAuthor).where(
                models.DBAuthor.name == author_info.get("name"))
        ):
            raise HTTPException(
                status_code=400,
                detail="Author with this name already exists"
            )
    except HTTPException as e:
        print(e)

    db_author = models.DBAuthor(
        **author_info
    )
    db.add(db_author)
    db.flush()

    if db_books:
        for book in db_books:
            db_book = models.DBBook(
                **book.model_dump(),
                author_id=db_author.id,
            )
            db.add(db_book)

    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def update_author(
        db: Session,
        author_id_to_update: int,
        author_update_info: schemas.AuthorUpdate
):
    author = db.get(models.DBAuthor, author_id_to_update)

    if not author:
        raise ValueError("There is no such author")

    books = author_update_info.books
    author_update_info = author_update_info.model_dump(
        exclude_unset=True, exclude={"books"}
    )
    for field, value in author_update_info.items():
        setattr(author, field, value)

    db.flush()
    author.books = []

    if books:
        for book in books:
            db_book = db.get(models.DBBook, book.id)
            if db_book:
                author.books.append(db_book)

    db.commit()
    db.refresh(author)

    return author


def partial_update_author(
        db: Session,
        author_id_to_update: int,
        author_update_info: schemas.AuthorPartialUpdate
):
    author = db.get(models.DBAuthor, author_id_to_update)
    author = update_function(
        author, author_update_info, exclude={"books"}, exclude_unset=True
    )

    if author_update_info.books:
        for book in author_update_info.books:
            db_book = db.get(models.DBBook, book.id)
            if db_book:
                author.books.append(db_book)

    db.commit()
    db.refresh(author)

    return author


def delete_author(
        db: Session,
        author_id
):
    author = db.get(models.DBAuthor, author_id)

    db.delete(instance=author)
    db.commit()

    return f"{author.name} was Successfully deleted!!!"


def get_all_books(
        db: Session,
        author_id: int | None,
        skip: int = 0,
        limit: int = 10,
):
    queryset = select(models.DBBook).offset(skip).limit(limit)
    if author_id is not None:
        queryset = queryset.where(
            models.DBBook.author_id == author_id
        ).distinct()
    return db.scalars(queryset).all()


def get_book_by_id(
        db: Session,
        book_id: int
):
    return db.scalar(select(models.DBBook).where(models.DBBook.id == book_id))


def create_book(
        db: Session,
        book_info: schemas.BookCreate
):
    db_book = models.DBBook(
        **book_info.model_dump()
    )

    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book


def update_book(
        db: Session,
        book_id: int,
        book_update_info: schemas.BookUpdate
):
    db_book = db.get(models.DBBook, book_id)
    db_book = update_function(db_book, book_update_info, exclude_unset=True)

    db.commit()
    db.refresh(db_book)

    return db_book


def partial_update_book(
        db: Session,
        book_id: int,
        book_update_info: schemas.BookPartialUpdate
):
    db_book = db.get(models.DBBook, book_id)
    db_book = update_function(db_book, book_update_info, exclude_unset=True)

    db.commit()
    db.refresh(db_book)

    return db_book


def delete_book(
        db: Session,
        book_id: int
):
    db_book = db.get(models.DBBook, book_id)

    db.delete(db_book)
    db.commit()

    return db_book
