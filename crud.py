from sqlalchemy.orm import Session

from db_library import models
import schemas


def create_author(db: Session, author: schemas.Author):
    db_author = models.DBAuthor(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author

def get_author(db: Session):
    return db.query(models.DBAuthor).filter(models.DBAuthor.id == id).first()

def get_all_authors(db: Session):
    authors = db.query(models.DBAuthor).offset(skip=0).limit(10)
    authors = authors.all()

    return authors

