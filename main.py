from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal


app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/authors/", response_model=list[schemas.AuthorList])
def read_authors(
        db: Session = Depends(get_db),
        skip: int | None = None,
        limit: int | None = None
):
    return crud.get_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/", response_model=schemas.AuthorList)
def read_author_by_id(
        author_id: int,
        db: Session = Depends(get_db),
):
    if author_id:
        return crud.get_author(db=db, author_id=author_id)
    else:
        raise HTTPException(status_code=404, detail="Author id is required")


@app.post("/authors/", response_model=schemas.AuthorList)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    author_by_name = crud.get_author_by_name(db=db, name=author.name)

    if author_by_name:
        raise HTTPException(
            status_code=400,
            detail="Such name for Author already exists"
        )

    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=list[schemas.BookList])
def read_books(
        author_id: int | None = None,
        skip: int | None = None,
        limit: int | None = None,
        db: Session = Depends(get_db)
):
    return crud.get_books(author_id=author_id, skip=skip, limit=limit, db=db)


@app.post("/books/", response_model=schemas.BookList)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(book=book, db=db)
