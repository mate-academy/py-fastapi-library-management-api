from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, HTTPException
from sqlmodel import Session
from fastapi import Depends
import crud
import schemas
from database import engine, Base

app = FastAPI()

def create_db_and_tables():
    Base.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

def get_session():
    with Session(engine) as session:
        yield session

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

@app.get("/authors/", response_model=List[schemas.Author])
def read_authors(db: Session = Depends(get_session), skip: int = 0, limit: int = 10):
    return crud.get_all_authors(db=db, skip=skip, limit=limit)

@app.get("/authors/{author_id}", response_model=schemas.Author)
def author_retrieve(author_id: int, db: Session = Depends(get_session)):
    return crud.get_author(db=db, author_id=author_id)

@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_session)):
    author = crud.get_author_name(db=db, name=author.name)
    if author:
        raise HTTPException(status_code=400, detail="Author already exists")

    return crud.create_author(db=db, author=author)

@app.get("/books/", response_model=List[schemas.Book])
def reed_author(db: Session = Depends(get_session), author_id: int | None = None, skip: int = 0, limit: int = 10):
    return crud.get_all_books(db=db, author_id=author_id , skip=skip, limit=limit)

@app.get("/books/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_session)):
    return crud.get_book(db=db, book_id=book_id)

@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_session)):
    return crud.create_book(db=db, book=book)
