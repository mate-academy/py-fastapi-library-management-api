from sqlalchemy.orm import Session
from . import models, schemas

def create_author(db: Session, author: schemas.AuthorCreate) -> models.Author:
    db_author: models.Author = models.Author(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author
