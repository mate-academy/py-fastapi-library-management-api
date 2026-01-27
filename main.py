from fastapi import FastAPI, Depends, HTTPException
from database import engine
from sqlalchemy.orm import Session

import crud
import schemas, models
from database import SessionLocal


models.Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db),
):

    db_author = crud.get_author_by_name(db, name=author.name)

    if db_author:
        raise HTTPException(
            status_code=400,
            detail=f"Author with name '{author.name}' already exists.",
        )

    return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=list[schemas.Author])
def get_authors_list(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return crud.get_all_authors(db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def get_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_id(db, id=author_id)

    if db_author is None:
        raise HTTPException(
            status_code=404,
            detail=f"Author not found.",
        )

    return db_author


@app.post("/books", response_model=schemas.Book)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db),
):
    db_author = crud.get_author_by_id(db, id=book.author_id)
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")

    db_book = crud.get_book_by_title(db, title=book.title)

    if db_book:
        raise HTTPException(
            status_code=400,
            detail=f"Book with title '{book.title}' already exists.",
        )

    return crud.create_book(db=db, book=book)


@app.get("/books/", response_model=list[schemas.Book])
def get_books(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return crud.get_all_books(db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/books/", response_model=list[schemas.Book])
def get_author_books(
        author_id: int,
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100
):
    return crud.get_book_by_author(db, author_id=author_id, skip=skip, limit=limit)
