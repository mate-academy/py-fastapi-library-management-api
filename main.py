from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session

import crud
import schemas
from db.database import SessionLocal

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(db: Session = Depends(get_db),
                 skip: int = Query(0, alias="page"),
                 limit: int = Query(0, alias="size")):
    return crud.get_all_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def get_single_author(author_id: int, db: Session = Depends(get_db)):
    return crud.get_author(db, author_id)


@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    db_author = crud.get_authors_by_name(db=db, name=author.name)
    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Author with this name already exists"
        )
    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(db: Session = Depends(get_db),
               author_id: int = None,
               skip: int = Query(0, alias="page"),
               limit: int = Query(0, alias="size")
               ):
    return crud.get_all_books(db=db, author_id=author_id, skip=skip, limit=limit)


@app.post("/books/", response_model=schemas.Book)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
):
    return crud.create_book(db=db, book=book)
