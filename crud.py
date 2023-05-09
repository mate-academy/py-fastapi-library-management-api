from sqlalchemy.orm import Session, Query

from schemas import AuthorCreate, BookCreate

from models import Author, Book


def create_author(db: Session, author: AuthorCreate) -> Author:
    author = Author(name=author.name, bio=author.bio)
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


def get_author_by_id(db: Session, author_id: int) -> Query:
    return db.query(Author).filter_by(id=author_id).first()


def get_autor_by_name(db: Session, autor_name: str) -> Author:
    return db.query(Author).filter_by(name=autor_name).first()


def get_author_list(db: Session, skip: int = 0, limit: int = 100) -> Query:
    return db.query(Author).offset(skip).limit(limit).all()


def create_book(db: Session, book: BookCreate, author_ids: list[int]) -> Book:
    authors_objs = db.query(Author).filter(Author.id.in_(author_ids)).all()
    book = Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        authors=authors_objs,
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def get_book_by_id(db: Session, book_id: int) -> Query:
    return db.query(Book).filter_by(id=book_id).first()


def get_book_list(
    db: Session, skip: int = 0, limit: int = 100, author_id: int | None = None
) -> Query:
    query = db.query(Book)

    if author_id:
        query = query.filter(Author.id == author_id)
    return query.offset(skip).limit(limit).all()
