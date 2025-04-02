from sqlalchemy.orm import Session

from db.models import AuthorModel, BookModel
from schemas import AuthorCreate, BookCreate


def get_author_by_name(db: Session, name: str):
    return db.query(AuthorModel).filter(AuthorModel.name==name).first()


def get_authors(db: Session, skip: int = 0, limit: int = 10):
    return db.query(AuthorModel).offset(skip).limit(limit).all()


def get_total_authors_count(db: Session):
    return db.query(AuthorModel).count()


def get_one_author(db: Session, author_id: int):
    author = db.query(AuthorModel).filter(AuthorModel.id==author_id).first()

    return author


def create_author(db: Session, author: AuthorCreate):
    db_author = AuthorModel(
        name=author.name,
        bio=author.bio,
    )

    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_book_by_title(db: Session, title: str):
    return db.query(BookModel).filter(BookModel.title==title).first()


def get_total_books_count(db: Session):
    return db.query(BookModel).count()


def get_books(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        author_id: int | None = None
):
    queryset = db.query(BookModel)
    if author_id:
        queryset = db.query(BookModel).filter(
            BookModel.author_id == author_id)

    return queryset.offset(skip).limit(limit).all()

def get_one_book(db: Session, book_id: int):
    book = db.query(BookModel).filter(BookModel.id==book_id).first()

    return book

def create_book(db: Session, book: BookCreate):
    db_book = BookModel(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id,
    )

    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book