from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal, Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root() -> dict:
    return {"message": "Hello World"}


@app.get("/book/", response_model=list[schemas.Book])
def read_book_list(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    author_id: int | None = None,
):
    return crud.get_all_books(
        db=db, skip=skip, limit=limit, author_id=author_id
    )


@app.get("/book/{book_id}/", response_model=schemas.Book)
def read_single_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db=db, book_id=book_id)

    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return db_book


@app.post("/book/", response_model=schemas.Book)
def create_book(
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
):
    db_book = crud.get_book_by_title(db=db, title=book.title)

    if db_book:
        raise HTTPException(
            status_code=400, detail="Such title for Book already exists"
        )
    return crud.create_book(db=db, book=book)


@app.get("/author/", response_model=list[schemas.Author])
def read_author_list(
    db: Session = Depends(get_db), skip: int = 0, limit: int = 100
):
    return crud.get_all_authors(db=db, slip=skip, limit=limit)


@app.get("/author/{author_id}/", response_model=schemas.Author)
def read_single_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db=db, author_id=author_id)

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.post("/author/", response_model=schemas.Author)
def create_author(
    author: schemas.AuthorCreate,
    db: Session = Depends(get_db),
):
    db_author = crud.get_author_by_name(db=db, name=author.name)

    if db_author:
        raise HTTPException(
            status_code=400, detail="Such name for author already exists"
        )
    return crud.create_author(db=db, author=author)
