import schemas

import crud
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from db import models


from db.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.post("/author/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_name(author_name=author.name, db=db)
    if db_author:
        raise HTTPException(status_code=400, detail="Author already exists")
    return crud.create_author(db, author)


@app.get("/author/", response_model=list[schemas.Author])
def read_authors(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    return crud.get_authors_list(db, skip=skip, limit=limit)


@app.get("/author/{author_id}/", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_id(author_id=author_id, db=db)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.post("/book/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db, book)


@app.get("/books/", response_model=list[schemas.Book])
def get_books(
        limit: int = 100,
        skip: int = 0,
        db: Session = Depends(get_db)
):
    return crud.get_book_list(db, skip, limit)


@app.get("/book/{author_id}/", response_model=list[schemas.Book])
def read_book(author_id: int, db: Session = Depends(get_db)):
    return crud.filter_book(db, author_id=author_id)
