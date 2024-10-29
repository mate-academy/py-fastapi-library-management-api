from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from db import schemas, crud
from db.engine import SessionLocal


app = FastAPI()

def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_all_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_single_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.post("/author/create/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(author=author, db=db)


@app.get("/books/", response_model=list[schemas.Book])
def get_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_all_books(db, skip=skip, limit=limit)


@app.post("/book/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)


@app.get("/author/{author_id}/books/", response_model=list[schemas.Book])
def read_books_by_author(
    author_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    return crud.get_books_by_author(db, author_id=author_id, skip=skip, limit=limit)
