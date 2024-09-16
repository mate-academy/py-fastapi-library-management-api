from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal

import schemas
import crud
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db_conn() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "hello!"}


@app.get("/authors/", response_model=list[schemas.Author])
def get_all_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db_conn)):
    return crud.get_authors(db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def get_author(author_id: int, db: Session = Depends(get_db_conn)):
    author = crud.get_author(db=db, author_id=author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.get("/books/", response_model=list[schemas.Book])
def get_all_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db_conn)):
    return crud.get_books(db, skip=skip, limit=limit)


@app.get("/authors/{book_author_id}/books", response_model=list[schemas.Book])
def get_books(
        book_author_id: int,
        db: Session = Depends(get_db_conn)
):
    return crud.get_books_by_author(db=db, author_id=book_author_id)


@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db_conn)
):
    return crud.create_author(db=db, author=author)


@app.post("/books/", response_model=schemas.Book)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db_conn)
):
    return crud.create_book(db=db, book=book)
