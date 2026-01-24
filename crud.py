from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

import models
import schemas


def no_entity(code: int, name: str) -> HTTPException:
    raise HTTPException(
        status_code=code,
        detail=f"{name} not found",
    )


def get_list_authors(db: Session, skip: int = 0, limit: int = 100):
    return db.scalars(select(models.DBAuthor).offset(skip).limit(limit)).all()


def get_author_by_id(db: Session, author_id: int):
    return db.get(models.DBAuthor, author_id)


def get_author_by_name(db: Session, name: str):
    return db.scalar(
        select(models.DBAuthor).where(models.DBAuthor.name == name)
    )


def create_author(
        db: Session,
        author_data: schemas.AuthorCreate
):
    existed_author = get_author_by_name(db, author_data.name)
    if existed_author:
        raise HTTPException(
            status_code=400,
            detail="Author already exists",
        )
        return None

    db_author = models.DBAuthor(
        **author_data.model_dump()
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def update_author(
        db: Session,
        author_id: int,
        author_data: schemas.AuthorUpdate):
    db_item = get_author_by_id(db, author_id)
    if not db_item:
        no_entity(code=400, name="Author")
        return None
    author_data = author_data.model_dump(exclude_unset=True)
    for key, value in author_data.items():
        setattr(db_item, key, value)

    db.commit()
    db.refresh(db_item)
    return db_item


def delete_author(db: Session, author_id: int):
    db_item = get_author_by_id(db, author_id)
    if not db_item:
        no_entity(code=400, name="Author")
        return None

    db.delete(db_item)
    db.commit()

    return db_item


def get_list_of_books(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        author_id: int = None,
):
    query = select(models.DBBook)

    if author_id:
        query = query.where(models.DBBook.id == author_id)

    result = db.scalar(query.offset(skip).limit(limit)).all()
    return result



def get_book_by_id(db: Session, book_id: int):
    return db.execute(
        select(models.DBBook)
        .options(joinedload(models.DBBook.author))
        .where(models.DBBook.id == book_id)
    ).scalar_one_or_none()


def get_book_by_title(db: Session, title: str):
    return db.scalar(
        select(models.DBBook).where(models.DBBook.title == title)
    )


def create_book(
        db: Session,
        book_data: schemas.BookCreate
):
    existing_book = get_book_by_title(db, book_data.title)
    if existing_book:
        raise HTTPException(
            status_code=400,
            detail="Book already exists",
        )
        return None
    db_item = models.DBBook(**book_data.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item


def update_book(
        db: Session,
        book_id: int,
        book_data: schemas.BookUpdate
):
    db_item = get_book_by_id(db, book_id)

    if not db_item:
        no_entity(400, name="Book")
        return None

    book_data = book_data.model_dump(exclude_unset=True)
    for key, value in book_data.items():
        setattr(db_item, key, value)

    db.commit()
    db.refresh(db_item)

    return db_item


def delete_book(db: Session, book_id: int):
    db_item = get_book_by_id(db, book_id)

    if not db_item:
        no_entity(400, name="Book")
        return None

    db.delete(db_item)
    db.commit()

    return db_item
