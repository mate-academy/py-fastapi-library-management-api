from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import schemas
import crud
from database import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root() -> dict:
    return {"main page": "Page"}


@app.get(
    "/authors/",
    response_model=List[schemas.AuthorList]
)
def get_all_authors(
        skip: int = Query(0, alias="page"),
        limit: int = Query(10, alias="size"),
        db: Session = Depends(get_db),
) -> List[schemas.AuthorList]:
    return crud.get_all_authors(db=db, skip=skip, limit=limit)


@app.get(
    "/authors/{author_id}/",
    response_model=schemas.AuthorBase
)
def get_single_author(
        author_id: int,
        db: Session = Depends(get_db)
) -> schemas.AuthorBase:
    db_author = crud.get_author(db=db, author_id=author_id)

    if db_author is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )

    return db_author


@app.post(
    "/authors/",
    response_model=schemas.AuthorList
)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db),
) -> schemas.AuthorList:
    db_author = crud.get_author_by_name(
        db=db,
        name=author.name
    )

    if db_author:
        raise HTTPException(
            status_code=400,
            detail="This name is already exist!"
        )

    return crud.create_author(db=db, author=author)


@app.get(
    "/books/",
    response_model=List[schemas.BookList]
)
def get_all_books(
        db: Session = Depends(get_db),
        skip: int = Query(0, alias="page"),
        limit: int = Query(10, alias="size"),
        author_id: Optional[int] = None,
) -> List[schemas.BookList]:
    return crud.get_book_list(
        db=db,
        skip=skip,
        limit=limit,
        author_id=author_id
    )


@app.post(
    "/books/",
    response_model=schemas.BookList
)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
) -> schemas.BookList:
    return crud.create_book(db=db, book=book)


@app.get(
    "/books/{book_id}/",
    response_model=schemas.BookList
)
def get_single_book(
        book_id: int,
        db: Session = Depends(get_db)
) -> schemas.BookList:
    db_book = crud.get_book(db=db, book_id=book_id)

    if db_book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return db_book
