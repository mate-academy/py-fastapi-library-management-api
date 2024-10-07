from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import crud
import models
import schemas


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root() -> dict:
    return {"message": "Welcome to the library!"}


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_name(db, name=author.name)
    if db_author:
        raise HTTPException(
            status_code=400,
            detail="An author with this name already exists"
        )
    return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    authors = crud.get_authors(db, skip=skip, limit=limit)
    return authors


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id=book.author_id)
    if not db_author:
        raise HTTPException(
            status_code=400,
            detail="Author with such ID does not exist"
        )
    return crud.create_book(db=db, book=book)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
        author_id: int | None = None,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    books = crud.get_books(db, skip=skip, limit=limit, author_id=author_id)

    if not books:
        raise HTTPException(status_code=404, detail="No books found")

    return books
