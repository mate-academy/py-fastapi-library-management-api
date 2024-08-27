from sqlalchemy.orm import Session

from app.models import (
    DBAuthor,
    DBBook
)
from app.serializers import (
    AuthorCreate,
    BookCreate
)
from app.config import settings


def get_author_list(
        db: Session,
        skip: int = settings.DEFAULT_SKIP_VALUE,
        limit: int = settings.DEFAULT_LIMIT_VALUE
) -> list[DBAuthor]:
    return db.query(DBAuthor).offset(skip).limit(limit).all()


def get_author_by_name(
        db: Session,
        name: str
) -> DBAuthor:
    return db.query(DBAuthor).filter(
        DBAuthor.name == name
    ).first()


def get_author_by_id(
        db: Session,
        author_id: int
) -> DBAuthor:
    return db.query(DBAuthor).filter(
        DBAuthor.id == author_id
    ).first()


def create_author(
        db: Session,
        author: AuthorCreate
) -> DBAuthor:
    db_author = DBAuthor(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_books_list(
        db: Session,
        skip: int = settings.DEFAULT_SKIP_VALUE,
        limit: int = settings.DEFAULT_LIMIT_VALUE
) -> list[DBBook]:
    return db.query(DBBook).offset(skip).limit(limit).all()


def create_book(
        db: Session,
        book: BookCreate
) -> DBBook:
    db_book = DBBook(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book


def get_books_by_author_id(
        db: Session,
        author_id: int,
        skip: int = settings.DEFAULT_SKIP_VALUE,
        limit: int = settings.DEFAULT_LIMIT_VALUE
) -> DBBook:
    query_set = db.query(DBBook)

    if author_id is not None:
        query_set = query_set.filter(
            DBBook.author_id == author_id
        )

    return query_set.offset(skip).limit(limit).all()
