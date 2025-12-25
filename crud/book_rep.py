from sqlalchemy.orm import Session

from database.models import BookModel
from schemas.books import BookCreateSchema


def add_book(db: Session, book_data: BookCreateSchema):
    book = BookModel(
        title=book_data.title,
        summary=book_data.summary,
        author_id=book_data.author_id,
    )

    db.add(book)
    db.commit()
    db.refresh(book)

    return book


def select_author_books(db: Session, limit: int = 10, skip: int = 0, author_id: int = None):
    books = db.query(BookModel).offset(skip).limit(limit)
    if author_id:
        books = books.filter(BookModel.author_id == author_id)

    return books.all()

