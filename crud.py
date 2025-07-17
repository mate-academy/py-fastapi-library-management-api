from sqlalchemy.orm import Session

import schemas
import models
from models import Author, Book


def get_all_authors(skip, limit, db: Session):
    return db.query(Author).offset(skip).limit(limit).all()

def get_author(db: Session, author_id: int):
    return db.query(Author).filter(Author.id == author_id).first()

def create_author(author: schemas.AuthorCreate, db: Session):
    author = models.Author(name=author.name, bio=author.bio)
    db.add(author)
    db.commit()
    db.refresh(author)
    return author

def get_all_books(skip, limit, db: Session):
    return db.query(Book).offset(skip).limit(limit).all()


