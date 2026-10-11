from sqlalchemy.orm import Session
import models, schemas


def add_author(db: Session, author: schemas.AddAuthor):
    db_author = models.Author(
        name=author.name,
        bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

def get_authors_list(db: Session, skip: int = 0, limit: int = 5):
    queryset = db.query(models.Author)
    return queryset.offset(skip).limit(limit).all()

def get_author_by_name(db: Session, name: str):
    return (
        db.query(
            models.Author
        ).filter(
            models.Author.name == name
        ).first()
    )

def get_author_by_id(db: Session, id: int):
    return (
        db.query(
            models.Author
        ).filter(
            models.Author.id == id
        ).first()
    )

def add_book(db: Session, book: schemas.AddBook):

    author = get_author_by_id(db, book.author_id)

    if author is None:
        return None

    db_book = models.Book(
        title = book.title,
        summary = book.summary,
        publication_date = book.publication_date,
        author_id = book.author_id
    )

    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_books_list(db: Session, skip: int = 0, limit: int = 5):
    queryset = db.query(models.Book)
    return queryset.offset(skip).limit(limit).all()

def get_books_by_author_id(db: Session, author_id: int):
    return (
        db.query(
            models.Book
        ).filter(
            models.Book.author_id == author_id
        ).all()
    )