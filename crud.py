from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

import schemas
from db import models


def get_all_authors(db: Session) -> list[models.DBAuthor]:
    return db.scalars(select(models.DBAuthor)).all()


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


def get_book_list(
    db: Session,
    title: str,
    summary: str,
    publication_date: date,
    author_id: int,
    author: str | None = None,
) -> list[models.DBAuthor]:
    stmt = select(models.DBAuthor)

    if author_id:
        stmt = stmt.where(models.DBAuthor.packaging_type == packaging_type)

    if cheese_type:
        stmt = stmt.join(models.DBCheeseType).where(
            models.DBCheeseType.name == cheese_type
        )

    return db.scalars(stmt).all()


def get_cheese_by_id(db: Session, cheese_id: int) -> models.DBCheese | None:
    return db.scalar(select(models.DBCheese).where(models.DBCheese.id == cheese_id))


def get_cheese_by_title(db: Session, title: str) -> models.DBCheese | None:
    return db.scalar(select(models.DBCheese).where(models.DBCheese.title == title))


def create_cheese(db: Session, cheese: schemas.CheeseCreate) -> models.DBCheese:
    db_cheese = models.DBCheese(
        cheese_type_id=cheese.cheese_type_id,
        title=cheese.title,
        price=cheese.price,
        packaging_type=cheese.packaging_type,
    )
    db.add(db_cheese)
    db.commit()
    db.refresh(db_cheese)

    return db_cheese
