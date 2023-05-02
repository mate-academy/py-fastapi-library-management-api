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
def root():
    return {"message": "Hello World"}


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
    db: Session = Depends(get_db), skip: int = 0, limit: int = 10
):
    return crud.get_author_list(db=db)[skip:skip + limit]


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def get_one_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author_by_id(db=db, author_id=author_id)

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    return author


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_name(db=db, name=author.name)

    if db_author:
        raise HTTPException(
            status_code=400, detail="Such author already exists"
        )

    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
    db: Session = Depends(get_db),
    author_id: int = None,
    skip: int = 0,
    limit: int = 10
):
    return crud.get_book_list(db=db, author_id=author_id)[skip:skip + limit]


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_id(db=db, author_id=book.author_id)

    if not db_author:
        raise HTTPException(
            status_code=404, detail="Such author doesn't exist"
        )

    return crud.create_book(db=db, book=book)
