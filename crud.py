from sqlalchemy.orm import Session
from models import Author, Book
from schemas import AuthorCreate, BookCreate

def get_authors(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Author).offset(skip).limit(limit).all()

def get_books(db: Session, skip: int = 0, limit: int = 10):
    query = db.query(Book)
    return query.offset(skip).limit(limit).all()

def create_author(db: Session, author: AuthorCreate):
    author = Author(name=author.name, bio=author.bio)
    db.add(author)
    db.commit()
    db.refresh(author)

    return author


def create_book(db: Session, book: BookCreate, author_id: int):
    book = Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=author_id,
    )
    db.add(book)
    db.commit()
    db.refresh(book)

    return book