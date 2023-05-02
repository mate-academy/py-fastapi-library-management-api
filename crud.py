from sqlalchemy.orm import Session

from schemas import AuthorBase, AuthorMain, AuthorCreate, BookBase, BookMain, BookCreate

from models import Author, Book


def create_author(db: Session, author: AuthorCreate):
    author = Author(name=author.name, bio=author.bio)
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


def get_autor_by_id(db: Session, autor_id):
    return db.query(Author).filter_by(id=autor_id).first()


def get_autor_by_name(db: Session, autor_name):
    return db.query(Author).filter_by(name=autor_name).first()


def get_author_list(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Author).offset(skip).limit(limit).all()


def create_book(db: Session, book: BookCreate):
    db_book = Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        authors=[db.query(Author).get(author_id) for author_id in book.author_ids],
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_book_by_id(db: Session, book_id):
    return db.query(Book).filter_by(id=book_id).first()


def get_bool_list(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Book).offset(skip).limit(limit).all()
