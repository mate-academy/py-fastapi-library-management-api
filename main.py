from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(author=author, db=db)

@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    authors = crud.get_authors(skip=skip, limit=limit, db=db)
    return authors

@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(id=author_id, db=db)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Not found")
    return db_author

@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_author = crud.get_author(id=book.author_id, db=db)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.create_book(book=book, db=db)

@app.get("/books/", response_model=list[schemas.Book])
def read_books(author_id: int=None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if author_id:
        return crud.filter_book(author_id=author_id, skip=skip, limit=limit, db=db)
    return crud.get_books(skip=skip, limit=limit, db=db)

@app.get("/books/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(id=book_id, db=db)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Not found")
    return db_book
