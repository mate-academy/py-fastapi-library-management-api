from sqlalchemy.orm import Session
from db import models
from schemas import schemas_author


def get_author(db: Session, author_id: int = None, skip: int = 0, limit: int = 10):
    if author_id is None:
        return db.query(models.Author).offset(skip).limit(limit).all()
    else:
        return db.query(models.Author).filter(models.Author.id == author_id).first()


def create_author(db: Session, create_authors: schemas_author.CreateAuthor):
    db_create_author = models.Author(
        name = create_authors.name,
        bio = create_authors.bio
    )
    db.add(db_create_author)
    db.commit()
    db.refresh(db_create_author)
    return db_create_author


def author_name(db: Session, name: str):
    return db.query(models.Author).filter(models.Author.name == name).first()