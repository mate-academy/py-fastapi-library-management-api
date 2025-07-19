from typing import Annotated, Type

from fastapi import FastAPI, Query, HTTPException, Depends
from sqlmodel import select, Session

from db.database import create_db_and_tables, get_session
from db.models import Author, Book

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/authors/")
def create_author(author: Author, session: Session = Depends(get_session)) -> Author:
    session.add(author)
    session.commit()
    session.refresh(author)
    return author


@app.get("/authors/")
def read_authors(
    session: Session = Depends(get_session),
    skip: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Author]:
    authors = session.exec(select(Author).offset(skip).limit(limit)).all()
    return authors


@app.get("/authors/{author_id}", response_model=Author)
def read_author(
        author_id: str,
        session: Session = Depends(get_session)
) -> Type[Author]:
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.delete("/authors/{author_id}")
def delete_author(
        author_id: str,
        session: Session = Depends(get_session)
) -> dict:
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    session.delete(author)
    session.commit()
    return {"ok": True}


@app.post("/books/")
def create_book(book: Book, session: Session = Depends(get_session)) -> Book:
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


@app.get("/books/")
def read_books(
    session: Session = Depends(get_session),
    skip: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Book]:
    books = session.exec(select(Author).offset(skip).limit(limit)).all()
    return books


@app.get("/books/{author_id}", response_model=list[Book])
def get_books_of_author(
        author_id: str,
        session: Session = Depends(get_session),
) -> list[Book] | None:
    statement = (select(Book).join(Book.author).where(author_id=author_id))
    return session.exec(statement).all() or None
