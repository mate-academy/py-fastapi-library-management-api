from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud, database, schemas

app = FastAPI()


def get_db() -> Session:
    db_session = database.SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()


@app.get("/")
def root() -> dict:
    return {"Message": "Welcome to library"}


@app.get("/authors/", response_model=list[schemas.AuthorInfo])
def read_authors(
    skip: int = 0, limit: int = 10, db_session: Session = Depends(get_db)
):
    return crud.get_all_authors(db_session=db_session)[skip : skip + limit]


@app.post("/authors/", response_model=schemas.AuthorInfo)
def create_author(
    author: schemas.AuthorCreate, db_session: Session = Depends(get_db)
):
    db_existing_author = crud.get_author_by_name(
        db_session=db_session, name=author.name
    )
    if db_existing_author:
        raise HTTPException(
            status_code=400, detail="Author with such name already exist"
        )
    return crud.create_author(db_session=db_session, author=author)


@app.get("/authors/{author_id}/", response_model=schemas.AuthorInfo)
def read_single_author(author_id: int, db_session: Session = Depends(get_db)):
    db_author = crud.get_author_by_id(db_session=db_session, author_id=author_id)

    if db_author is None:
        raise HTTPException(
            status_code=404, detail=f"Author with id {author_id} not found"
        )

    return db_author


@app.get("/books/", response_model=list[schemas.BookInfo])
def read_books(
    skip: int = 0,
    limit: int = 10,
    db_session: Session = Depends(get_db),
    author_id: int | None = None,
):
    books = crud.get_all_books(db_session=db_session, author_id=author_id)
    return books[skip : skip + limit]


@app.post("/books/", response_model=schemas.BookInfo)
def create_book(
    book: schemas.BookCreate, db_session: Session = Depends(get_db)
):
    return crud.create_book(db_session=db_session, book=book)
