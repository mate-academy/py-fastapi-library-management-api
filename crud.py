from fastapi import HTTPException
from sqlalchemy.orm import Session

import schemas
from db import models
from db.engine import engine
from db.models import Author
from main import app


def get_all_author(db: Session):
    return db.query(models.Author).all()


def get_all_books(db: Session):
    return db.query(models.Book).all()


def create_author(db: Session, author: schemas.CreateAuthor):
    db_author = models.Author(
        name=author.name,
        bio=author.bio,
        books=author.book,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


@app.patch("/author/{author_id}", response_model=models.Author)
def update_hero(author_id: int, author: schemas.UpdateAuthor):
    with Session(engine) as session:
        db_author = session.get(Author, author_id)
        if not db_author:
            raise HTTPException(status_code=404, detail="Author not found")
        author_data = author.dict(exclude_unset=True)
        for key, value in author_data.items():
            setattr(db_author, key, value)
        session.add(db_author)
        session.commit()
        session.refresh(db_author)
        return db_author


@app.delete("/author/{author_id}")
def delete_author(author_id: int):
    with Session(engine) as session:
        author = session.get(Author, author_id)
        if not author:
            raise HTTPException(status_code=404, detail="Author not found")
        session.delete(author)
        session.commit()
        return {"ok": True}


def create_books(db: Session, book: schemas.CreateBook):
    db_book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book
