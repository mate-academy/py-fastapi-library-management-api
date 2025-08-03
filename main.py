from fastapi import FastAPI
from fastapi.params import Depends, Query
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal
from schemas import AuthorCreate, BookCreate, BookUpdate

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----------------- Author block ---------------
@app.get("/authors", status_code=200)
def authors_list(
        skip: int = 0,
        limit: int = Query(default=10, le=100),
        db: Session = Depends(get_db)
):
    return crud.get_all_authors(db, skip, limit)


@app.get("/author/{author_id}", status_code=200)
def author_by_id(author_id: int, db: Session = Depends(get_db)):
    return crud.get_author_by_id(db, author_id)


@app.post("/author-create", status_code=201)
def author_create(author: AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db, author)


@app.put("/author-update/{author_id}", status_code=200)
def author_update(
        author_id: int,
        author: schemas.AuthorUpdate,
        db: Session = Depends(get_db)
):
    return crud.author_update(db, author_id, author)


@app.delete("/author-delete/{author_id}", status_code=204)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    return crud.author_delete(db, author_id)

# ----------------- Book block ---------------
@app.get("/books", status_code=200)
def get_all_books(
        skip: int = 0,
        limit: int = Query(default=10, le=100),
        db: Session = Depends(get_db)
):
    return crud.get_all_books(db, skip, limit)


@app.get("/book/{author_id}", status_code=200)
def get_book_by_author_id(author_id: int, db: Session = Depends(get_db)):
    return crud.get_book_by_author_id(db, author_id)


@app.post("/book-create", status_code=201)
def book_create(book: BookCreate, db: Session = Depends(get_db)):
    return crud.book_create(db, book)


@app.put("/book-update/{book_id}", status_code=200)
def book_update(book: BookUpdate, book_id: int, db: Session = Depends(get_db)):
    return crud.book_update(db, book_id, book)


@app.delete("/book/{book_id}", status_code=204)
def book_delete(book_id: int, db: Session = Depends(get_db)):
    return crud.book_delete(db, book_id)
