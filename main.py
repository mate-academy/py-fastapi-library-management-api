from fastapi import FastAPI, Depends, Query
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
async def root() -> dict:
    return {"message": "Hello World"}


@app.get("/authors/", response_model=list[schemas.Author])
async def get_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)) -> list[schemas.Author]:
    return crud.get_authors(db=db, skip=skip, limit=limit)


@app.post("/authors/", response_model=schemas.Author)
async def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)) -> schemas.Author:
    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=list[schemas.Book])
async def get_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)) -> list[schemas.Book]:
    return crud.get_books(db=db, skip=skip, limit=limit)


@app.get("/books/by_author/{author_id}", response_model=list[schemas.Book])
async def get_books_by_author(author_id: int, db: Session = Depends(get_db)) -> list[schemas.Book]:
    return crud.get_books_by_author(db=db, author_id=author_id)


@app.post("/books/", response_model=schemas.Book)
async def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)) -> schemas.Book:
    return crud.create_book(db=db, book=book, author_id=book.author_id)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id=author_id)
    return db_author
