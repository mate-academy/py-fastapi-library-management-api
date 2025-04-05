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

@app.post("/authors/", response_model=schemas.NumOfAuthor)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)

@app.get("/authors/", response_model=schemas.AuthorList)
def get_authors(db: Session = Depends(get_db)):
    authors = crud.get_authors(db=db)
    return {"authors": authors}
@app.get("/authors/{author_id}", response_model=schemas.NumOfAuthor)
def get_author_by_id(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_id(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author

@app.post("/authors/{author_id}/book", response_model=schemas.NumOfBook)
def create_book_for_author(author_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_id(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return crud.create_new_book_for_author(db=db, book=book)

@app.get("/books/", response_model=schemas.BookList)
def get_books(db: Session = Depends(get_db)):
    books = crud.get_books(db=db)
    return {"books": books}

@app.get("/book/{book_id}", response_model=schemas.NumOfBook)
def get_book_by_id(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book_by_id(book_id=book_id, db=db)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return db_book

@app.get("/book/author/{author_id}", response_model=schemas.NumOfBook)
def get_book_by_author_id(author_id: int, db: Session = Depends(get_db)):
    db_books = crud.get_book_by_id(author_id=author_id, db=db)
    if db_books is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return db_books




