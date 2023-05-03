from sqlalchemy.orm import Session
from db.models import Author, Book
from schemas import (AuthorCreate, BookCreate)


def get_all_authors(db: Session):
    return db.query(Author).all()


def create_author(
        db: Session,
        author: AuthorCreate
):
    db_author = Author(
        name=author.name,
        bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

