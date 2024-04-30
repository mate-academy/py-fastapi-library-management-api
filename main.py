import uvicorn
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException

import crud
import schemas
from database import SessionLocal


# creating fastAPI app
app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Define a route to serve a user
@app.get("/")
def read_root() -> dict:
    return {"Response": "simple FastAPI response"}


@app.get("/authors/", response_model=list[schemas.Author])
def get_authors(skip: int = 0,
                limit: int = 10,
                db: Session = Depends(get_db)) -> list | None:
    return crud.get_all_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def get_author_by_id(author_id: int,
                     db: Session = Depends(get_db)) -> schemas.Author:
    db_author = crud.get_author(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
) -> schemas.Author:
    db_author = crud.get_author_by_name(db=db, name=author.name)
    if db_author:
        raise HTTPException(status_code=400, detail="Author already exists")
    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=list[schemas.Book])
def get_books_list(skip: int = 0, limit: int = 10,
                   db: Session = Depends(get_db)) -> list | None:
    return crud.get_all_books(db=db, skip=skip, limit=limit)


@app.get("/books/{author_id}/", response_model=list[schemas.Book])
def get_books_by_author(author_id: int,
                        skip: int = 0, limit: int = 10,
                        db: Session = Depends(get_db)) -> list | None:
    db_record = crud.get_author(db=db, author_id=author_id)
    if not db_record:
        raise HTTPException(
            status_code=404,
            detail="Wrong author ID"
        )
    db_record = crud.confirm_book_by_author(db=db, author_id=author_id)
    if not db_record:
        raise HTTPException(
            status_code=404,
            detail="Author hasn't any books yet"
        )
    return crud.get_books_by_author(db=db, author_id=author_id,
                                    skip=skip, limit=limit)


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate,
                db: Session = Depends(get_db)) -> schemas.Book:
    return crud.create_book_by_author(db=db, book=book)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
