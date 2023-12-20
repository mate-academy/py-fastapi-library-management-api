from sqlalchemy.orm import Session

from db.models import DBAuthor
from schemas import AuthorCreate


def create_author(db: Session, author: AuthorCreate):
    db_author = DBAuthor(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_all_authors_with_pagination(db: Session, skip: int = 0, limit: int = 10):
    authors = db.query(DBAuthor).offset(skip).limit(limit).all()
    return authors


def get_author_by_id(db: Session, author_id: int):
    return db.query(DBAuthor).filter(DBAuthor.id == author_id).first()


def get_author_by_name(db: Session, name: str):
    return db.query(DBAuthor).filter(DBAuthor.name == name).first()
