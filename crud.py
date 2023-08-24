from sqlalchemy.orm import Session
from data_base import models
from schemas import AuthorCreate, BookCreate


def get_all_authors(data_base: Session, page: int, size: int) -> list:
    return data_base.query(models.DBAuthor).offset(page).limit(size).all()


def get_author_by_name(data_base: Session, name: str):
    return (
        data_base.query(models.DBAuthor).
        filter(models.DBAuthor.name == name).first()
    )


def get_author(data_base: Session, author_id: int):
    return data_base.query(models.DBAuthor).filter(models.DBAuthor.id == author_id).first()


def create_author(data_base: Session, author: AuthorCreate):
    data_base_author = models.DBAuthor(
        name=author.name,
        bio=author.bio
    )
    data_base.add(data_base_author)
    data_base.commit()
    data_base.refresh(data_base_author)

    return data_base_author


def get_all_books(
        data_base: Session,
        page: int,
        size: int,
        author_id: int | None = None,
):
    query = data_base.query(models.DBBook)

    if author_id:
        query = query.filter(models.DBBook.author_id == author_id)

    return query.offset(page).limit(size).all()


def get_book(data_base: Session, book_id: int):
    return data_base.query(models.DBBook).filter(models.DBBook.id == book_id).first()


def create_book(data_base: Session, book: BookCreate):
    data_base_book = models.DBBook(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id,
    )
    data_base.add(data_base_book)
    data_base.commit()
    data_base.refresh(data_base_book)
    return data_base_book
