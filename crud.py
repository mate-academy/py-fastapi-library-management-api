from sqlalchemy.orm import Session
import models, schemas


def get_author(db: Session, id: int):
    return db.query(models.DBAuthor).filter(models.DBAuthor.id == id).first()


def get_authors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.DBAuthor).offset(skip).limit(limit).all()


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.DBAuthor(name=author.name, bio=author.bio)

    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author



def get_book(db: Session, id: int):
    return db.query(models.DBBook).filter(models.DBBook.id == id).first()


def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.DBBook).offset(skip).limit(limit).all()


def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.DBBook(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id,
    )

    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def filter_book(db: Session, skip: int = 0, limit: int = 100, author_id: int = None):
    query = db.query(models.DBBook)
    if author_id:
        return query.offset(skip).limit(limit).filter(models.DBBook.author_id == author_id)
    return query.offset(skip).limit(limit).all()
