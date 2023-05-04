from app import models, schemas
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import desc

from app.utils import get_author_or_404, get_book_or_404


def get_author_by_id(db: Session, author_id: int):
    return (
        db.query(models.Author).filter(models.Author.id == author_id).first()
    )


def get_author_list(name: str, db: Session, skip: int = 0, limit: int = 5):
    db_authors = db.query(models.Author)
    if name:
        db_authors = db_authors.filter(models.Author.name.ilike(f"%{name}%"))
    return db_authors.offset(skip).limit(limit).all()


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(**author.dict())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def update_author(db: Session, author_id: int, author: schemas.AuthorUpdate):
    db_author = get_author_or_404(db=db, author_id=author_id)
    db_author.name = author.name
    db_author.bio = author.bio

    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def partial_update_author(
    db: Session, author_id: int, author: schemas.AuthorPartialUpdate
):
    db_author = get_author_or_404(author_id=author_id, db=db)
    db_author.name = author.name if author.name else db_author.name
    db_author.bio = author.bio if author.bio else db_author.bio

    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def delete_author(db: Session, author_id: int):
    db_author = get_author_or_404(db=db, author_id=author_id)
    db.delete(db_author)
    db.commit()


def get_book_by_id(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def get_book_list(
    title: str,
    db: Session,
    sort_parameter: str = None,
    sort_asc: bool = True,
    skip: int = 0,
    limit: int = 5,
):
    db_books = db.query(models.Book)
    if title:
        db_books = db_books.filter(models.Book.title.ilike(f"%{title}%"))
    if sort_parameter:
        if sort_asc:
            db_books = db_books.order_by(sort_parameter)
        else:
            db_books = db_books.order_by(desc(sort_parameter))

    return db_books.offset(skip).limit(limit).all()


def get_book_list_by_author_id(db: Session, author_id: int):
    return (
        db.query(models.Book).filter(models.Book.author_id == author_id).all()
    )


def create_book(db: Session, book: schemas.BookCreate, author_id: int):
    db_book = models.Book(**book.dict(), author_id=author_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def update_book(db: Session, book: schemas.BookUpdate, book_id: int):
    db_book = get_book_or_404(db=db, book_id=book_id)
    db_book.title = book.title
    db_book.summary = book.summary
    db_book.publication_date = book.publication_date

    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def partial_update_book(
    db: Session, book: schemas.BookPartialUpdate, book_id: int
):
    db_book = get_book_or_404(book_id=book_id, db=db)
    db_book.title = book.title if book.title else db_book.title
    db_book.summary = book.summary if book.summary else db_book.summary
    db_book.publication_date = (
        book.publication_date
        if book.publication_date
        else db_book.publication_date
    )

    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int):
    db_book = get_book_or_404(book_id=book_id, db=db)
    db.delete(db_book)
    db.commit()
