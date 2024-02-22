from sqlalchemy.orm import Session

from db import models
import schemas


def get_author_by_name(db: Session, author_name: str):
    return db.query(models.DBAuthor).filter(models.DBAuthor.name == author_name).first()


def get_all_authors(db: Session):
    return db.query(models.DBAuthor).all()


def create_author(db: Session, new_author: schemas.AuthorCreate):
    db_author = models.DBAuthor(
        name=new_author.name,
        bio=new_author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author
