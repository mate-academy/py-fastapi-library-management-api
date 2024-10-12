from sqlalchemy.orm import Session
from models import DbAuthor, DbBook
import schemas


def get_all_authors(db: Session, skip: int = 0, limit: int = 10):
    return db.query(DbAuthor).offset(skip).limit(limit).all()


def get_author(db: Session, author_id: int):
    return (
        db.query(DbAuthor).filter(DbAuthor.id == author_id).first()
    )


def create_author(db: Session, author: schemas.AuthorCreate):
    author = DbAuthor(
        name=author.name,
        bio=author.bio,
    )
    db.add(author)
    db.commit()
    db.refresh(author)

    return author


def get_books_list(
        db: Session,
        author_name: str | None = None,
        skip: int = 0,
        limit: int = 10
):
    queryset = db.query(DbAuthor).offset(skip).limit(limit)

    if author_name is not None:
        queryset = queryset.filter(DbBook.author.has(name=author_name))

    return queryset.all()


def get_book(db: Session, book_id: int):
    return db.query(DbBook).filter(DbBook.id == book_id).first()


def create_book(db: Session, book: schemas.BookCreate):
    db_book = DbBook(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book