from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session

from database import engine, SessionLocal, Base
import crud
import schemas


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library Management API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post(
    "/authors/",
    response_model=schemas.Author,
    status_code=status.HTTP_201_CREATED
)
def create_author(
        author: schemas.AuthorCreate, db: Session = Depends(get_db)
):
    return crud.create_author(db=db, author=author)

@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
        skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    return crud.get_authors(db=db, skip=skip, limit=limit)

@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    return crud.get_author(db=db, author_id=author_id)

@app.post(
    "/authors/{author_id}/books/",
    response_model=schemas.Book,
    status_code=status.HTTP_201_CREATED
)
def create_book_for_author(
        author_id: int,
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
):
    return crud.create_book(db=db, book=book, author_id=author_id)

@app.get("/books/", response_model=list[schemas.Book])
def read_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_books(db=db, skip=skip, limit=limit)

@app.get("/authors/{author_id}/books/", response_model=list[schemas.Book])
def read_books_by_author(author_id: int, db: Session = Depends(get_db)):
    return crud.get_books_by_author(db=db, author_id=author_id)