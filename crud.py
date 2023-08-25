from sqlalchemy.orm import Session

from db.models import DBBook, DBAuthor
from schemas import BookCreate, AuthorCreate


def get_all_books(db: Session):
    return db.query(DBBook).all()


def get_books_by_author_id(db: Session, author_id: int):
    queryset = db.query(DBBook)
    if author_id:
        queryset = queryset.filter(DBBook.author_id == author_id)

    return queryset.all()


def create_book(db: Session, book: BookCreate):
    db_book = DBBook(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_all_authors(db: Session):
    return db.query(DBAuthor).all()


def get_author(db: Session, author_id: int):
    return db.query(DBAuthor).filter(
        DBAuthor.id == author_id
    ).first()


def create_author(db: Session, author: AuthorCreate):
    db_author = DBAuthor(
        name=author.name,
        bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author
