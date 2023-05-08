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
def root() -> dict:
    return {"message": "Hello World"}


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(db: Session = Depends(get_db), skip=0, limit=2):
    return crud.get_all_authors(db=db, skip=skip, limit=limit)


@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    return crud.create_author(db=db, author=author)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_author(
        author_id: int,
        db: Session = Depends(get_db)
):
    author = crud.get_detail_author(db=db, author_id=author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    return author


@app.put("/authors/{author_id}/", response_model=schemas.Author)
def update_author(
        author_id: int,
        author: schemas.AuthorUpdate,
        db: Session = Depends(get_db)
):
    updated_author = crud.update_author(db, author_id, author)
    if not updated_author:
        raise HTTPException(status_code=404, detail="Author not found")
    return updated_author


@app.delete("/authors/{author_id}/", response_model=schemas.Author)
def delete_author(
        author_id: int,
        db: Session = Depends(get_db)
):
    deleted_author = crud.delete_author(db, author_id)

    if not deleted_author:
        raise HTTPException(status_code=404, detail="Author not found")
    return deleted_author


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
        author_id: int | None = None,
        db: Session = Depends(get_db),
        skip=1,
        limit=5
):
    return crud.get_all_books(
        db=db, author_id=author_id, skip=skip, limit=limit
    )


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)
