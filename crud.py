from sqlalchemy.orm import Session
from models import Author, Book
from schemas import AuthorCreate, BookCreate


def get_author_by_id(db: Session, author_id: int):
    return db.query(Author).filter(Author.id == author_id).first()


def get_author_by_name(db: Session, name: str):
    return (
        db.query(Author).filter(Author.name == name).first()
    )


def get_all_authors(db: Session, skip: int = 0, limit: int = 5):
    return db.query(Author).offset(skip).limit(limit)


def create_author(db: Session, author: AuthorCreate):
    db_author = Author(
        name=author.name,
        bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_all_books(db: Session,
                  author_id: int | None = None,
                  skip: int = 0,
                  limit: int = 5):
    queryset = db.query(Book)

    if author_id:
        queryset = queryset.filter(Book.author_id == author_id)

    return queryset.offset(skip).limit(limit)


def create_book(db: Session, book: BookCreate):
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
