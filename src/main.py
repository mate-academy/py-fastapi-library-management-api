from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from src import schemas, crud, models
from src.database import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root() -> dict:
    return {"message": "Hello World"}


@app.get("/authors/", response_model=list[schemas.AuthorResponseSchema])
def get_authors_list(db: Session = Depends(get_db)):
    return crud.get_all_authors(db)


@app.post("/authors/", response_model=schemas.AuthorResponseSchema)
def create_author(
    author: schemas.AuthorCreateResponseSchema,
    db: Session = Depends(get_db),
):
    db_author = crud.get_author_by_name(db=db, name=author.name)
    if db_author:
        raise HTTPException(
            status_code=409,
            detail="Such name for Author already exists"
        )
    return crud.create_author(db=db, author=author)


@app.get("/authors/{author_id}/", response_model=schemas.AuthorResponseSchema)
def get_author_details(author_id: int, db: Session = Depends(get_db)):
    author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if not author:
        raise HTTPException(
            status_code=404,
            detail="Author with the given ID was not found"
        )
    return author


@app.get("/books/", response_model=list[schemas.BookResponseSchema])
def read_books(db: Session = Depends(get_db)):
    return crud.get_all_books(db)


@app.post("/books/", response_model=schemas.BookResponseSchema)
def create_author(
    book: schemas.BookCreateResponseSchema,
    db: Session = Depends(get_db),
):
    db_book = crud.get_book_by_title(db=db, title=book.title)
    if db_book:
        raise HTTPException(
            status_code=400,
            detail="Such title name for Book already exists"
        )
    return crud.create_book(db=db, book=book)


@app.get("/books/{author_id}/", response_model=list[schemas.BookResponseSchema])
def get_book_details(author_id: int, db: Session = Depends(get_db)):
    books = db.query(models.Book).filter(models.Book.author_id == author_id).all()
    if not books:
        raise HTTPException(
            status_code=404,
            detail="Books for the given author ID were not found"
        )
    return books
