from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from db.engine import SessionLocal

from fastapi_pagination import paginate

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root() -> dict:
    return {"Hello": "World"}


@app.get("/authors/", response_model=list[schemas.Author])
def get_authors(db: Session = Depends(get_db)):
    return paginate(crud.get_all_authors(db=db))


@app.get("/authors/{author_id}", response_model=schemas.Author)
def get_authors_by_id(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_id(db=db, author_id=author_id)
    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Such author already exist"
        )
    return db_author


@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=list[schemas.Book])
def get_books(author_id: int = None, db: Session = Depends(get_db)):
    if author_id is None:
        return paginate(crud.get_all_books(db=db))
    return paginate(crud.get_all_books(db=db, author_id=author_id))


@app.post("/books/", response_model=schemas.Book)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
):
    return crud.create_book(db=db, book=book)
