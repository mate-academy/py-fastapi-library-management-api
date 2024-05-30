from sqlalchemy.orm import Session
import models
from schemas import AuthorCreate, BookCreate


def get_all_authors(
        db: Session,
        skip: int | None,
        limit: int | None
) -> list[models.Author]:

    queryset = db.query(models.Author)
    if skip:
        queryset = queryset.offset(skip)
    if limit:
        queryset = queryset.limit(limit)
    return queryset.all()


def get_author_by_id(db: Session, author_id: int) -> models.Author:
    return db.query(models.Author).filter(
        models.Author.id == author_id).first()


def get_author_by_name(db: Session, author_name: str) -> models.Author:
    return db.query(models.Author).filter(
        models.Author.name == author_name).first()


def create_author(db: Session, author: AuthorCreate) -> models.Author:
    db_author = models.Author(
        name=author.name,
        bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_all_books(
        db: Session,
        skip: int | None,
        limit: int | None,
        author_id: int | None
) -> list[models.Book]:

    queryset = db.query(models.Book)
    if skip:
        queryset = queryset.offset(skip)
    if limit:
        queryset = queryset.limit(limit)
    if author_id:
        queryset = queryset.filter(models.Book.author_id == author_id)

    return queryset.all()


def get_book_by_title(db: Session, book_title: str) -> models.Book:
    return db.query(models.Book).filter(
        models.Book.title == book_title).first()


def create_book(db: Session, book: BookCreate) -> models.Book:
    db_book = models.Book(
        title=book.title,
        summary=book.summary,
        author_id=book.author_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
