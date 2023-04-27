from sqlalchemy.orm import Session
import models, schemas


def get_author(db: Session, author_id: int):
    return db.query(models.Author).filter(models.Author.id == author_id).first()


def get_author_by_name(db: Session, name: str):
    return db.query(models.Author).filter(models.Author.name == name).first()


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_all_authors(db: Session, skip: int, limit: int):
    return db.query(models.Author).offset(skip).limit(limit).all()


def get_book_by_title(db: Session, title: str):
    return db.query(models.Book).filter(models.Book.title == title).first()


def get_books_by_author(db: Session, author_id: int):
    return db.query(models.Book).filter(models.Book.author_id == author_id).all()


def create_book(db: Session, book: schemas.BookCreate):
    db_author = get_author_by_name(db, book.author)
    if not db_author:
        db_author = create_author(db, schemas.AuthorCreate(name=book.author, bio=None))
    db_book = models.Book(title=book.title, publication_date=book.publication_year, author_id=db_author.id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_all_books(db: Session, skip: int, limit: int):
    return db.query(models.Book).offset(skip).limit(limit).all()
