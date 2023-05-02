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


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get(
    "/authors/",
    response_model=list[schemas.AuthorWithBooks]
)
async def read_authors(db: Session = Depends(get_db)):
    return crud.get_all_authors_with_pagination(db=db)


@app.get(
    "/authors/{author_id}",
    response_model=schemas.AuthorWithBooks
)
async def read_author(
        author_id: int,
        db: Session = Depends(get_db)
):
    db_author = crud.get_author_by_id(
        db=db,
        author_id=author_id
    )

    if db_author is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )
    return db_author


@app.post("/authors/", response_model=schemas.Author)
async def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    if crud.get_author_by_name:
        raise HTTPException(
            status_code=400,
            detail="Author with this name already exists"
        )
    return crud.create_author(db=db, author=author)


@app.post("/books/", response_model=schemas.Book)
async def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
):
    return crud.create_book(db=db, book=book)


@app.get("/books/", response_model=list[schemas.Book])
async def read_books(
        db: Session = Depends(get_db),
        author_id: str | None = None
):
    return crud.get_all_books_with_pagination(
        db=db,
        author_id=author_id
    )


@app.post("/authors/{author_id}/books/")
def create_book_for_author(
        author_id: int,
        book: schemas.BookCreateForAuthor,
        db: Session = Depends(get_db)
):
    return crud.create_book_for_author(
        db=db,
        book=book,
        author_id=author_id
    )
