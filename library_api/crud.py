from sqlalchemy.orm import Session

from models import Author, Book


def create_author(db: Session, author: Author):
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


def get_list_of_authors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Author).offset(skip).limit(limit).all()


def get_author_by_id(db: Session, author_id: int):
    return db.query(Author).filter(Author.id == author_id).first()


def create_book_by_author(db: Session, book: Book):
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def get_list_of_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Book).offset(skip).limit(limit).all()


def filter_books_by_author_id(
    db,
    author_id: int,
    skip: int = 0,
    limit: int = 100,
):
    return (
        db.query(Book)
        .filter(Book.author_id == author_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
