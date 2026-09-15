from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import Base, SessionLocal, engine
from models import DBAuthor, DBBook

# 1. Initialize the FastAPI application instance
app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db() -> Session:

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# 2. Define a path operation decorator (GET request to the root "/" path)
@app.get("/")
def root() -> dict:
    # 3. Return a JSON-serializable dictionary
    return {"message": "Hello World"}


@app.get("/books/", response_model=list[schemas.Book])
def get_books(
    skip: int = 0,
    limit: int = 100,
    author_id: int | None = None,
    db: Session = Depends(get_db),
):
    return crud.get_all_books(db=db, skip=skip, limit=limit, author_id=author_id)


@app.post("/books/", response_model=schemas.Book)
def post_book(
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
):
    return crud.create_book(db=db, book=book)


@app.post("/authors/", response_model=schemas.Author)
def post_authors(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)


@app.get("/authors/")
def get_authors(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return crud.get_all_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def get_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id)
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.post("/authors/{author_id}/books", response_model=schemas.Book)
def create_book_for_author(
    author_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)
):
    return crud.create_book(db=db, book=book, author_id=author_id)
