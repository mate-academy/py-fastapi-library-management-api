from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from db.models import Author, Book
from db.schemas import AuthorCreate, BookCreate


def get_all_authors_by_skip_and_limit(db: Session, skip: int, limit: int):
    stmt = select(Author)

    if skip is not None:
        stmt = stmt.offset(skip)

    if limit is not None:
        stmt = stmt.limit(limit)

    return db.execute(stmt).scalars().all()

def create_new_author(db: Session, author: AuthorCreate):
    db_author = Author(name=author.name, bio=author.bio)

    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author

def get_author_by_id(db: Session, item_id: int):
    return db.scalar(select(Author).where(Author.id == item_id))

def create_book_for_author(db: Session, book: BookCreate):
    author = db.scalar(select(Author).where(Author.id == book.author_id))
    if author is None:
        raise HTTPException(status_code=404, detail="Author with such id does not exist")

    db_book = Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id
    )

    db.add(db_book)
    db.commit()

    db.refresh(db_book)

    return db_book



def get_books_by_filtering(db: Session, skip: int | None, limit: int | None, author_id: int | None):
    stmt = select(Book)

    if author_id is not None:
        stmt = stmt.where(Book.author_id == author_id)

    if skip is not None:
        stmt = stmt.offset(skip)

    if limit is not None:
        stmt = stmt.limit(limit)

    return db.execute(stmt).scalars().all()
