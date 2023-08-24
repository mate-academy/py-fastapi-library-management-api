from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from database.models import AuthorDB, BookDB
from schemas import AuthorCreate, AuthorUpdate, BookBaseCreate, BookUpdate


def create_author(db: Session, author: AuthorCreate):
    db_author = AuthorDB(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def read_all_authors(db: Session):
    return db.query(AuthorDB).all()


def update_author(db: Session, author_id: int, author: AuthorUpdate):
    db_author = db.query(AuthorDB).filter(AuthorDB.id == author_id).first()

    if db_author:
        for key, value in author.model_dump().items():
            setattr(db_author, key, value)
        db.commit()
        db.refresh(db_author)
        return db_author
    else:
        raise NoResultFound("Author not found")


def get_author_by_name(db: Session, name: str):
    return db.query(AuthorDB).filter(AuthorDB.name == name).first()


def create_book(db: Session, book: BookBaseCreate):
    db_book = BookDB(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book


def read_all_books(db: Session):
    return db.query(BookDB).all()


def update_book(db: Session, book_id: int, book: BookUpdate):
    db_book = db.query(BookDB).filter(BookDB.id == book_id).first()

    if db_book:
        for key, value in book.model_dump().items():
            setattr(db_book, key, value)
        db.commit()
        db.refresh(db_book)
        return db_book
    else:
        raise NoResultFound("Book not found")


def get_book_by_id(db: Session, book_id: int):
    return db.query(BookDB).filter(BookDB.id == book_id).first()
