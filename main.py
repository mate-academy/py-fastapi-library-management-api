from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
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


@app.post("/author/create/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    check = crud.search_by_name(db=db, name=author.name)
    if check:
        raise HTTPException(
            status_code=400,
            detail="Such author is in database"
        )
    return crud.create_new_author(author_data=author, db=db)


@app.get("/author/{author_id}", response_model=schemas.Author)
def search_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.search_author_by_id(db=db, pk=author_id)

    if author:
        return author
    raise HTTPException(status_code=400, detail="Not Found")


@app.post("/book/create/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    book = crud.create_book(db=db, book=book)

    if book is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found",
        )

    return book


@app.get("/authors/", response_model=list[schemas.Author])
def get_authors(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    return crud.get_authors(
        db=db,
        skip=skip,
        limit=limit,
    )


@app.get("/books/", response_model=list[schemas.Book])
def get_books(
    skip: int = 0,
    limit: int = 10,
    author_id: int | None = None,
    db: Session = Depends(get_db),
):
    return crud.get_books(
        db=db,
        skip=skip,
        limit=limit,
        author_id=author_id,
    )
