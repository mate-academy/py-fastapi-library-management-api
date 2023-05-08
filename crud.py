from sqlalchemy.orm import Session

import models
import schemas


def get_all_authors(db: Session):
    return db.query(models.Author).all()


def create_author(db: Session, author: schemas.Author):
    db_author = models.Author(
        name=author.name,
        bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_detail_author(db: Session, author_id: int):
    return (
        db.query(models.Author).filter(models.Author.id == author_id).first()
    )


def update_author(db: Session, author_id: int, **kwargs):
    author_to_update = db.query(models.Author).filter(models.Author.id == author_id).first()
    