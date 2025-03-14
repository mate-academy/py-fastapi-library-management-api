from sqlalchemy.orm import Session

from app.models import AuthorModel, BookModel
from app.schemas import CreateAuthorSchema, CreateBookSchema


def get_list_authors(db: Session, offset: int, limit: int):
    return db.query(AuthorModel).offset(offset).limit(limit).all()


def get_author(db: Session, author_id: int):
    return db.query(AuthorModel).filter(AuthorModel.id == author_id).first()


def create_author(db: Session, data: CreateAuthorSchema):
    new_author = AuthorModel(
        name=data.name,
        bio=data.bio
    )
    db.add(new_author)
    db.commit()
    db.refresh(new_author)

    return new_author


def create_book(db: Session, data: CreateBookSchema):
    new_book = BookModel(
        title=data.title,
        summary=data.summary,
        publication_data=data.publication_data,
        author_id=data.author_id,
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book


def get_list_books(db: Session, offset: int, limit: int, author_id: int):
    query = db.query(BookModel)

    if author_id:
        query = query.filter(BookModel.author_id == author_id)

    return query.offset(offset).limit(limit).all()
