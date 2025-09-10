from sqlalchemy.orm import Session

from models import Author, Book
from schemas import AuthorCreate, BookCreate


def get_all_authors(db: Session) -> list[type[Author]]:
    return db.query(Author).all()


def get_author_by_id(db: Session, id: int) -> type[Author]:
    return db.query(Author).filter(Author.id == id).first()


def create_author_db(db: Session, author: AuthorCreate):
    new_author = Author(
        name=author.name,
        bio=author.bio,
    )
    db.add(new_author)
    db.commit()
    db.refresh(new_author)

    return new_author


def get_all_books(
        db: Session,
        author_id: int | None = None
) -> list[type[Book]]:
    queryset = db.query(Book)
    if author_id is not None:
        queryset = queryset.filter(Book.author.has(id=author_id))

    return queryset.all()


def get_book_by_id(db: Session, id: int) -> type[Book]:
    return db.query(Book).filter(Book.id == id).first()


def create_book_db(db: Session, book: BookCreate):
    new_book = Book(**book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book
