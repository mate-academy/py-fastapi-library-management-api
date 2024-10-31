from sqlalchemy.orm import Session

from models import DBBook, DBAuthor
import schemas


def get_author_by_id(db: Session, author_id: int):
    return (
        db.query(DBAuthor).
        filter(DBAuthor.id == author_id).
        first()
    )

def get_author_by_name(db: Session, author_name: str):
    return (
        db.query(DBAuthor).
        filter(DBAuthor.name == author_name).
        first()
    )

def author_create(db: Session, author: schemas.AuthorCreate):
    db_author = DBAuthor(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author

def get_all_authors(db: Session, page: int = 0, limit: int = 10):
    return db.query(DBAuthor).offset(page).limit(limit).all()

def get_all_books(
        db: Session,
        author_id: int = None,
        page: int = 0,
        limit: int = 10
):
    if author_id:
        queryset = (db.query(DBBook).
         filter(DBBook.author_id == author_id).
         offset(page).
         limit(limit))
    else:
        queryset = db.query(DBBook).offset(page).limit(limit)

    return queryset

def create_book(db: Session, book: schemas.BookCreate):
    db_book = DBBook(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book
