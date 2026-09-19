from sqlalchemy.orm import Session, joinedload
import models
import schemas


def get_all_authors(db: Session):
    return db.query(models.DBAuthor).options(joinedload(models.DBAuthor.books)).all()

def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.DBAuthor(**author.model_dump())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

def create_book_for_author(db: Session, book: schemas.BookCreate, author_id: int):
    db_book = models.DBBook(**book.model_dump(), author_id=author_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.DBBook).offset(skip).limit(limit).all()
