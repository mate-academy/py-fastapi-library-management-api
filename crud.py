from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

import schemas
from db import models


def get_all_authors(
    db: Session, skip: int = 0, limit: int = 10
) -> list[models.DBAuthor]:
    stmt = select(models.DBAuthor).offset(skip).limit(limit)
    return db.scalars(stmt).all()


def get_author_by_id(db: Session, author_id: int) -> models.DBAuthor | None:
    return db.scalar(select(models.DBAuthor).where(models.DBAuthor.id == author_id))


def create_author(db: Session, author: schemas.AuthorCreate) -> models.DBAuthor:
    db_author = models.DBAuthor(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_author_by_name(db: Session, name: str) -> models.DBAuthor | None:
    return db.scalar(select(models.DBAuthor).where(models.DBAuthor.name == name))
