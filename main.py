from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, Base, engine
import crud
import schemas
import models

app = FastAPI()

@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/authors", response_model=list[schemas.AuthorRead])
def list_authors(
        skip: int = 0,
        limit: int = 2,
        db: Session = Depends(get_db),
):
    return crud.get_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=schemas.AuthorRead)
def get_author_by_id(
        author_id: int,
        db: Session = Depends(get_db),
):
    author = crud.get_author(db=db, author_id=author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.post("/authors", response_model=schemas.AuthorRead)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    return crud.create_author(db=db, author=author)


@app.get("/books", response_model=list[schemas.BookRead])
def list_books(
    skip: int = 0,
    limit: int = 2,
    author_id: int | None = None,
    db: Session = Depends(get_db),
):
    return crud.get_books(
        db=db,
        skip=skip,
        limit=limit,
        author_id=author_id,
    )


@app.post("/books", response_model=schemas.BookRead)
def create_book(
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
):
    return crud.create_book(db=db, book=book)


