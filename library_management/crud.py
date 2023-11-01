from sqlalchemy.orm import Session

from library_management import models
from library_management.schemas import AuthorCreate


def get_all_authors(db: Session):
    return db.query(models.Author).all()


def create_author(db: Session, author: AuthorCreate):
    db_author = models.Author(
        name=author.name,
        bio=author.bio,
        books=author.books,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author
