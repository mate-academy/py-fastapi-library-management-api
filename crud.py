from sqlalchemy import select
from sqlalchemy.orm import Session

import schemas
from models import Author


def get_authors(db: Session, skip: int = 0, limit: int = 100):
    stmt = select(Author).offset(skip).limit(limit)
    result = db.execute(stmt)
    return result.scalars().all()


def get_author_by_name(db: Session, name: str):
    stmt = select(Author).where(Author.name == name)
    result = db.execute(stmt)
    return result.scalar_one_or_none()


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = Author(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_author_by_id(db: Session, author_id: int):
    stmt = select(Author).where(Author.id == author_id)
    result = db.execute(stmt)
    return result.scalar_one_or_none()
