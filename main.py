from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library Management API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_author(db=db, author=author)
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Author could not be created") from exc


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return crud.get_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.post("/authors/{author_id}/books/", response_model=schemas.Book)
def create_book_for_author(
    author_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)
):
    db_author = crud.get_author(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.create_book_for_author(db=db, author_id=author_id, book=book)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
    skip: int = 0,
    limit: int = 100,
    author_id: int | None = None,
    db: Session = Depends(get_db),
):
    if author_id is not None:
        return crud.get_books_by_author(
            db=db, author_id=author_id, skip=skip, limit=limit
        )
    return crud.get_books(db=db, skip=skip, limit=limit)

