from sqlalchemy.orm import Session
import models
import schemas


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.DBAuthor(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_author(db: Session, author_id: int):
    return db.query(models.DBAuthor).filter(models.DBAuthor.id == author_id).first()


def get_authors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.DBAuthor).offset(skip).limit(limit).all()


def update_author(db: Session, author_id: int, author: schemas.AuthorCreate):
    db_author = db.query(models.DBAuthor).filter(models.DBAuthor.id == author_id).first()
    db_author.name = author.name
    db_author.bio = author.bio
    db.commit()
    db.refresh(db_author)
    return db_author


def delete_author(db: Session, author_id: int):
    db_author = db.query(models.DBAuthor).filter(models.DBAuthor.id == author_id).first()
    db.delete(db_author)
    db.commit()
    return db_author


def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.DBBook(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_book(db: Session, book_id: int):
    return db.query(models.DBBook).filter(models.DBBook.id == book_id).first()


def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.DBBook).offset(skip).limit(limit).all()


def update_book(db: Session, book_id: int, book: schemas.BookCreate):
    db_book = db.query(models.DBBook).filter(models.DBBook.id == book_id).first()
    db_book.title = book.title
    db_book.summary = book.summary
    db_book.publication_date = book.publication_date
    db_book.author_id = book.author_id
    db.commit()
    db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int):
    db_book = db.query(models.DBBook).filter(models.DBBook.id == book_id).first()
    db.delete(db_book)
    db.commit()
    return db_book
