from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import HTTPException, Response, status

import models, schemas, utils


def get_author(db: Session, author_id: int):
    return db.query(models.DBAuthor).filter(models.DBAuthor.id == author_id).first()


def get_author_list(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    author_name: str | None = None,
    sort_field: str | None = None,
):
    queryset = db.query(models.DBAuthor)
    if author_name is not None:
        queryset = queryset.filter(models.DBAuthor.name.contains(author_name))
    if sort_field is not None:
        if sort_field.startswith("-"):
            sort_field = sort_field[1:] + " desc"
        queryset = queryset.order_by(text(sort_field))
    return queryset.offset(skip).limit(limit).all()


def create_author(
    db: Session,
    author: schemas.AuthorCreate
):
    new_author = models.DBAuthor(
        name=author.name,
        bio=author.bio,
    )
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author


def get_author_by_name(db: Session, authorname: str):
    return db.query(models.DBAuthor).filter(models.DBAuthor.name == authorname).first()


def get_book(db: Session, book_id: int):
    return db.query(models.DBBook).filter(models.DBBook.id == book_id).first()


def get_book_list(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    author_id: int | None = None,
    book_title: str | None = None,
    sort_field: str | None = None
):
    queryset = db.query(models.DBBook)
    if author_id is not None:
        queryset = queryset.filter(models.DBBook.author_id == author_id)
    if book_title is not None:
        queryset = queryset.filter(models.DBBook.title.contains(book_title))
    if sort_field is not None:
        if sort_field.startswith("-"):
            sort_field = sort_field[1:] + " desc"
        queryset = queryset.order_by(text(sort_field))
    return queryset.offset(skip).limit(limit).all()


def create_book(db: Session, book: schemas.BookCreate):
    new_book = models.DBBook(**book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


def get_book_by_title(db: Session, title: str):
    return db.query(models.DBBook).filter(models.DBBook.title == title).first()


def patch_book(
    book_id: int,
    db: Session,
    book: schemas.BookCreate
):
    db_book = get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(
            status_code=404,
            detail="Book was not found"
        )
    book_data = book.dict(exclude_unset=True)
    for key, val in book_data.items():
        setattr(db_book, key, val)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def delete_book(book_id: int, db: Session):
    db_book = get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(
            status_code=404,
            detail="Book was not found"
        )
    db.delete(db_book)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def patch_author(
    author_id: int,
    db: Session,
    author: schemas.AuthorCreate
):
    db_author = get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(
            status_code=404,
            detail="Author was not found"
        )
    author_data = author.dict(exclude_unset=True)
    for key, val in author_data.items():
        setattr(db_author, key, val)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def delete_author(author_id: int, db: Session):
    db_author = get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(
            status_code=404,
            detail="Author was not found"
        )
    db.delete(db_author)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def get_user_by_email(email: str, db: Session):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = utils.get_password_hash(user.password)
    user = models.User(
        email=user.email,
        hashed_pass=hashed_password
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
