from sqlalchemy.orm import Session

from db import models
import schemas


def get_all_authors(db: Session):
    return db.query(models.Author).all()

def get_author_type_by_name(db: Session, name: str):
    return db.query(models.Author).filter(models.Author.name == name).first()

def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author

def get_authors_list(db: Session,
                    name: str | None = None,
                    bio: schemas.Author | None = None,):
    queryset = db.query(models.Author)

    if name is not None:
        queryset = queryset.filter(
            models.Author.name == name.value
        )
    if bio is not None:
        queryset = queryset.filter(models.Author.bio.has(name=bio))

    return queryset.all()

def get_book(db: Session, author_id: int):
    return db.query(models.Book).filter(models.Book.id == author_id).first()

def create_book(db: Session, book: schemas.BookCreate):
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