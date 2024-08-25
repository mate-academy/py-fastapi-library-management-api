from sqlalchemy.orm import Session

from database import models, schemas


def get_all_authors(db: Session, skip: int = 0, limit: int = 10) -> any:
    return db.query(models.Author).offset(skip).limit(limit).all()


def get_author(db: Session, author_id: int) -> any:
    return db.query(models.Author).filter(
        models.Author.author_id == author_id
    ).first()


def create_author(db: Session, author: schemas.AuthorCreate) -> any:
    db_author = models.Author(
        name=author.name,
        bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_all_books(
        db: Session, author_id: int, skip: int = 0, limit: int = 10
) -> any:
    queryset = db.query(models.Book)

    if author_id:
        queryset = queryset.filter(models.Book.author_id.has == author_id)

    return queryset.offset(skip).limit(limit).all()


def get_book(db: Session, book_id: int) -> any:
    return db.query(models.Book).filter(models.Book.book_id == book_id).first()


def create_book(db: Session, book: schemas.BookCreate) -> any:
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
