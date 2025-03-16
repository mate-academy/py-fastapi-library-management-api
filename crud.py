from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi import HTTPException

from models import AuthorModel, BookModel
from schemas import AuthorRequestSchema, BookRequestSchema


def get_all_authors(db: Session, page: int, per_page: int):
    return db.query(AuthorModel).offset(
        per_page * (page - 1)
    ).limit(per_page).all()


def create_author(db: Session, data: AuthorRequestSchema) -> AuthorModel:
    author = AuthorModel(
        name=data.name,
        bio=data.bio
    )
    try:
        db.add(author)
        db.commit()
        db.refresh(author)
        return author
    except IntegrityError:
        raise ValueError


def get_all_books(
        db: Session,
        page: int,
        per_page: int,
        author_id: int | None
):
    queryset = db.query(BookModel)
    if author_id is not None:
        queryset = queryset.where(BookModel.author_id == author_id)
    queryset = queryset.offset(
            per_page * (page - 1)
        ).limit(per_page)
    return queryset


def get_author(db: Session, author_id: int) -> AuthorModel | None:
    return db.get(AuthorModel, author_id)


def get_book(db: Session, book_id: int) -> BookModel | None:
    return db.get(BookModel, book_id)


def create_book(db: Session, data: BookRequestSchema) -> BookModel | None:
    author = get_author(db, data.author_id)
    if author is None:
        raise HTTPException(
            status_code=400,
            detail="No such author!"
        )
    book = BookModel(
        title=data.title,
        summary=data.summary,
        publication_date=data.publication_date,
        author=author,
    )
    try:
        db.add(book)
        db.commit()
        db.refresh(book)
        return book
    except IntegrityError:
        raise ValueError
