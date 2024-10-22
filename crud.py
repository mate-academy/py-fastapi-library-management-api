from sqlalchemy.orm import Session

import models
import schemas


def get_all_authors(skip: int, limit: int, db: Session):
    return db.query(models.Author).offset(skip).limit(limit).all()


def get_all_books(db: Session, skip: int = 0, limit: int = 5, author_id: int = None):
    queryset = db.query(models.Book)

    if author_id:
        queryset = queryset.filter(models.Book.author_id == int(author_id))

    queryset = queryset.offset(skip).limit(limit).all()

    return queryset


def get_author_from_db(db: Session, author_id: int):
    return db.query(models.Author).filter(models.Author.id == author_id).first()


def create_author_db(author: schemas.AuthorCreate, db: Session):
    db_author = models.Author(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def create_book_db(book: schemas.BookCreate, db: Session):
    db_book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book
