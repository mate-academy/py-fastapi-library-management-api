from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud, schemas, models
from app.database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/authors/", response_model=list[schemas.AuthorResponse])
def read_authors(
    db: Annotated[Session, Depends(get_db)],
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
):

    return crud.get_all_authors(db=db, skip=skip, limit=limit)


@app.post("/authors/", response_model=schemas.AuthorResponse)
def create_author(
    author: schemas.AuthorCreate,
    db: Annotated[Session, Depends(get_db)],
):
    db_author = crud.get_author_by_name(db=db, author_name=author.name)

    if db_author:
        raise HTTPException(
            status_code=400, detail="Author with this name already exist"
        )

    return crud.create_author(db=db, author=author)


@app.get("/authors/{author_id}/", response_model=schemas.AuthorResponse)
def read_single_author(db: Annotated[Session, Depends(get_db)], author_id: int):
    db_author = crud.get_author_by_id(db=db, author_id=author_id)

    if not db_author:
        raise HTTPException(status_code=400, detail="Author not found")

    return db_author


@app.get("/books/", response_model=list[schemas.BookResponse])
def read_books(
    db: Annotated[Session, Depends(get_db)],
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    author_id: int | None = None,
):

    return crud.get_all_books(db=db, skip=skip, limit=limit, author_id=author_id)


@app.post("/books/", response_model=schemas.BookResponse)
def create_book(db: Annotated[Session, Depends(get_db)], book: schemas.BookCreate):
    return crud.create_book(db=db, book=book)
