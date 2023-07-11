from typing import Optional, List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from library import crud, schemas
from library.database import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[schemas.AuthorList])
def read_authors(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
) -> List[schemas.AuthorList]:
    return crud.get_all_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/", response_model=schemas.AuthorList)
def read_single_author(
    author_id: int,
    db: Session = Depends(get_db)
) -> schemas.AuthorList:
    db_author = crud.get_author(db=db, author_id=author_id)

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.post("/authors/", response_model=schemas.AuthorBase)
def create_author(
    author: schemas.AuthorCreate,
    db: Session = Depends(get_db),
) -> schemas.AuthorBase:
    db_author = crud.get_author_by_name(db=db, name=author.name)
    if db_author:
        raise HTTPException(
            status_code=400, detail="Such name for Author already exists"
        )
    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=list[schemas.BookList])
def read_books(
    db: Session = Depends(get_db),
    author_id: Optional[int] = None
) -> List[schemas.BookList]:
    return crud.get_all_books(db=db, author_id=author_id)


@app.post("/books/", response_model=schemas.BookList)
def create_book(
    book: schemas.BookCreate,
    db: Session = Depends(get_db)
) -> schemas.BookBase:
    return crud.create_book(db=db, book=book)
