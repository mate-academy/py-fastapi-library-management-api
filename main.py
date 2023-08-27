from fastapi import FastAPI, Depends, HTTPException, Query
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
    return {"message": "Hello World 🌍! There is my "
                       "first app using FastAPI ✨"}


@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors_list(
        skip: int = Query(0, description="Skip records"),
        limit: int = Query(10, description="Limit records"),
        db: Session = Depends(get_db)
):
    return crud.get_all_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def get_author_detail(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_id(db=db, author_id=author_id)

    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.post("/books/", response_model=schemas.Book)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
):
    db_author = crud.get_author_by_id(db=db, author_id=book.author_id)
    if not db_author:
        raise HTTPException(
            status_code=400,
            detail="Invalid data provided. Author with this id doesn't exist!"
        )
    return crud.create_book(db=db, book=book)


@app.get("/books/", response_model=list[schemas.Book])
def read_authors_list(
        author_id: int | None = None,
        skip: int = Query(0, description="Skip records"),
        limit: int = Query(10, description="Limit records"),
        db: Session = Depends(get_db)
):
    return crud.get_all_books(
        db=db, author_id=author_id, skip=skip, limit=limit
    )
