from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.post("/author/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    db_author = crud.get_author_by_name(db=db, name=author.name)

    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Such name for Author already exists"
        )
    return crud.create_author(db=db, author=author)


@app.get("/author/{skip}/{limit}/", response_model=list[schemas.Author])
def read_authors_with_pagination(skip: int, limit: int, db: Session = Depends(get_db)):
    db_author = crud.get_authors_with_pagination(db=db, skip=skip, limit=limit)
    return db_author


@app.get("/author/{pk}/", response_model=schemas.Author)
def read_authors_by_id(pk: int, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_id(db=db, pk=pk)
    return db_author

@app.get("/author/", response_model=list[schemas.Author])
def read_authors_list(db: Session = Depends(get_db)):
    db_author = crud.get_authors_with_pagination(db=db)
    return db_author

@app.post("/book/{name}/", response_model=schemas.Book)
def create_book(
        name: str,
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
):
    db_book = crud.get_book_by_title(db=db, title=book.title)

    if db_book:
        raise HTTPException(
            status_code=400,
            detail="Such Book already exists"
        )
    db_author = crud.get_author_by_name(db=db, name=name)
    if not db_author:
        raise HTTPException(
            status_code=400,
            detail="Author with this name not exist"
        )
    return crud.create_book_for_specific_author(db=db, book=book, name=name)


@app.get("/book/{skip}/{limit}/", response_model=list[schemas.Book])
def read_books_with_pagination(skip: int, limit: int, db: Session = Depends(get_db)) -> dict:
    db_author = crud.get_books_with_pagination(db=db, skip=skip, limit=limit)
    return db_author


@app.get("/book/", response_model=list[schemas.Book])
def filter_books_by_author_id(pk: int | None = None, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_id(pk=pk, db=db)
    if not db_author:
        raise HTTPException(
            status_code=200,
            detail=f"Author with this id not exist"
        )
    db_books = crud.get_filtered_books_by_author_id(author_id=pk, db=db)
    if not db_books:
        raise HTTPException(
            status_code=200,
            detail=f"Books list dont have any book related to Author with id {pk}"
        )
