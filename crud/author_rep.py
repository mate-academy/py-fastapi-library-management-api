from fastapi import HTTPException
from sqlalchemy.orm import Session

from database.models import AuthorModel
from schemas.authors import AuthorCreateSchema


def add_author(db: Session, author_data: AuthorCreateSchema):
    if db.query(AuthorModel).where(AuthorModel.name == author_data.name).count() != 0:
        raise HTTPException(
            status_code=409,
            detail=f"Author with {author_data.name} already exists"
        )

    author = AuthorModel(
        name=author_data.name,
        bio=author_data.bio
    )
    db.add(author)
    db.commit()
    db.refresh(author)

    return author


def select_author_by_id(
        author_id: int,
        db: Session
):
    author = db.query(AuthorModel).where(AuthorModel.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    return author


def select_authors(db: Session, skip: int = 0, limit: int = 10):
    authors = db.query(AuthorModel).offset(skip).limit(limit).all()
    return authors
