from sqlalchemy.orm import Session

import schemas
from db.models import DatabaseAuthor, DatabaseBook


def get_authors_list(db_session: Session, page: int = 1, page_size: int = 10):
    offset = (page - 1) * page_size
    query = db_session.query(
        DatabaseAuthor
    ).offset(offset).limit(page_size).all()
    return query


def get_author_by_name(db_session: Session, name: str):
    return db_session.query(
        DatabaseAuthor
    ).filter(DatabaseAuthor.name == name).first()


def get_author_detail(db_session: Session, author_id: int):
    return db_session.query(
        DatabaseAuthor
    ).filter(DatabaseAuthor.id == author_id).first()


def create_author(
        db_session: Session,
        author_schema_data: schemas.AuthorCreate
):
    db_author = DatabaseAuthor(
        **author_schema_data.model_dump()
    )
    db_session.add(db_author)
    db_session.commit()
    db_session.refresh(db_author)

    return db_author


def get_books_list(
        db_session: Session,
        page: int = 1,
        page_size: int = 10,
        author_id: int = None
):
    queryset = db_session.query(DatabaseBook)
    if author_id:
        queryset = db_session.query(
            DatabaseBook
        ).filter(DatabaseBook.author_id == author_id)
    offset = (page - 1) * page_size
    queryset = queryset.offset(offset).limit(page_size).all()

    return queryset


def get_book_by_title(db_session: Session, title: str):
    return db_session.query(
        DatabaseBook
    ).filter(DatabaseBook.title == title).first()


def create_book(db_session: Session, book_schema_data: schemas.BookCreate):
    db_book = DatabaseBook(
        **book_schema_data.model_dump()
    )
    db_session.add(db_book)
    db_session.commit()
    db_session.refresh(db_book)

    return db_book
