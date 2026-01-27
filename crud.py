from sqlalchemy import select
from sqlalchemy.orm import Session

import models
import schemas


def get_all_authors(db: Session):
    return db.scalars(select(models.Author)).all()

def create_author(db: Session, author: schemas.AuthorCreate):
    new_author = models.Author(
        name=author.name,
        bio=author.bio,
    )
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author

def get_author_by_name(db: Session, name: str):
    return(
        db.scalars(select(models.Author).where(models.Author.name == name))
    ).first()


def get_author_by_id(db: Session, author_id: int):
    return db.scalar(select(models.Author).where(models.Author.id == author_id))
