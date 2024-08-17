from sqlalchemy.orm import Session
import db_operation.models
import schemas


def get_all_books(db: Session, skip: int, limit: int):
    return db.query(db_operation.models.Book).offset(skip).limit(limit).all()


def get_all_authors(db: Session, skip: int, limit: int):
    return db.query(db_operation.models.Author).offset(skip).limit(limit).all()


def create_book(db: Session, book: schemas.BookCreateSchema):
    db_book = db_operation.models.Book(title=book.title, summary=book.summary,
                                       publication_date=book.publication_date,
                                       author_id=book.author_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def create_author(db: Session, author: schemas.AuthorCreateSchema):
    db_author = db_operation.models.Author(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_author_by_id(db: Session, author_id: int):
    return db.query(db_operation.models.Author).filter(
        db_operation.models.Author.id == author_id
    ).first()


def get_books_by_author_id(db: Session, author_id: int):
    return db.query(db_operation.models.Book).filter(
        db_operation.models.Book.author_id == author_id
    ).all()


def get_author_by_name(db: Session, name: str):
    return db.query(db_operation.models.Author).filter(
        db_operation.models.Author.name == name
    ).first()
