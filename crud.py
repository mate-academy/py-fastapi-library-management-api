from sqlalchemy.orm import Session

import models
from schemas import AuthorCreate


def get_all_authors(db: Session):
    return db.query(models.Author).all()


def create_author(db: Session, author: AuthorCreate):
    db_author = models.Author(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author
