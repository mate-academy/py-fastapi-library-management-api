from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database.engine import SessionLocal

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


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_name(db=db, name=author.name)
    if db_author:
        raise HTTPException(
            status_code=400, detail="Such name for Author already exists"
        )
    return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(db: Session = Depends(get_db)):
    return crud.read_all_authors(db=db)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    return crud.get_author_by_id(db=db, author_id=author_id)


@app.put("/authors/{author_id}", response_model=schemas.Author)
def update_author(
    author_id: int,
    author_update: schemas.AuthorUpdate,
    db: Session = Depends(get_db),
):
    db_author = crud.get_author_by_name(db=db, name=author_update.name)
    if not db_author:
        raise HTTPException(status_code=404, detail="Such Author not found")
    return crud.update_author(db=db, author_id=author_id, author=author_update)


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookBaseCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(db: Session = Depends(get_db)):
    return crud.read_all_books(db=db)


@app.get("/books/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    return crud.get_book_by_id(db=db, book_id=book_id)


@app.put("/books/{book_id}", response_model=schemas.Book)
def update_book(
    book_id: int,
    book_update: schemas.BookUpdate,
    db: Session = Depends(get_db),
):
    db_book = crud.get_book_by_id(db=db, book_id=book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Such Book not found")
    return crud.update_book(db=db, book_id=book_id, book=book_update)
