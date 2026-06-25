from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from db import crud, schemas
from db.database import SessionLocal, engine, Base


Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root() -> dict:
    return {"message": "Library Management API"}


@app.post("/authors/", response_model=schemas.Author)
def create_author(
    author: schemas.AuthorCreate,
    db: Session = Depends(get_db),
):
    db_author = crud.get_author_by_name(db, author.name)

    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Author with such name already exists",
        )

    return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=list[schemas.Author])
def get_authors(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.get_all_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def get_author(
    author_id: int,
    db: Session = Depends(get_db),
):
    db_author = crud.get_author_by_id(db=db, author_id=author_id)

    if db_author is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found",
        )

    return db_author


@app.post("/authors/{author_id}/books/", response_model=schemas.Book)
def create_book(
    author_id: int,
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
):
    db_author = crud.get_author_by_id(db=db, author_id=author_id)

    if db_author is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found",
        )

    return crud.create_book(db=db, book=book, author_id=author_id)


@app.get("/books/", response_model=list[schemas.Book])
def get_books(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.get_all_books(db=db, skip=skip, limit=limit)


@app.get("/books/by-author/{author_id}", response_model=list[schemas.Book])
def get_books_by_author(
    author_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.get_books_by_author_id(
        db=db,
        author_id=author_id,
        skip=skip,
        limit=limit,
    )
