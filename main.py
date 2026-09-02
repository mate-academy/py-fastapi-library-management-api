from fastapi import FastAPI, Depends

from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException

import crud
from db.database import Base, SessionLocal, engine

import schemas

Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.post("/author/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_name(db=db, name=author.name)
    if db_author:
        raise HTTPException(
            status_code=400, detail="Author with this name already exists"
        )

    return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=list[schemas.Author])
def get_authors(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int | None = None,
):
    return crud.get_authors_list(db=db, skip=skip, limit=limit)


@app.get("/author/{author_id}/", response_model=schemas.Author)
def get_single_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_id(db=db, author_id=author_id)

    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.post("/authors/{author_id}/books", response_model=schemas.Book)
def create_book(
    author_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)
):
    return crud.create_book(db=db, book=book, author_id=author_id)

@app.get("/books/", response_model=list[schemas.Book])
def get_books(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int | None = None,
):
    return crud.get_books_list(db=db, skip=skip, limit=limit)

@app.get("/authors/{author_id}/books", response_model=list[schemas.Book])
def get_books_by_author(
    author_id: int | None = None, db: Session = Depends(get_db)
):
    return crud.get_books_by_author_id(db, author_id=author_id)
