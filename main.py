from fastapi import FastAPI
from db.engine import session
from fastapi import Depends
from fastapi.responses import RedirectResponse
from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND

import schemas
import crud
app = FastAPI()


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


@app.get("/", include_in_schema=False)
def get_docs():
    return RedirectResponse(url="/docs")


@app.get("/authors/", response_model=list[schemas.Author])
def get_authors(db=Depends(get_db)):
    return crud.get_all_authors(db=db)


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db=Depends(get_db)):
    return crud.create_author(db=db, author=author)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def get_author_by_id(author_id, db=Depends(get_db)):
    author = crud.get_author_by_id(db=db, author_id=author_id)
    if not author:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Author with this id does not exist",
        )
    return author


@app.get("/books/", response_model=list[schemas.Book])
def get_books(db=Depends(get_db)):
    return crud.get_all_books(db=db)


@app.post("/books/", response_model=schemas.BookCreate)
def create_book(book: schemas.BookCreate, db=Depends(get_db)):
    return crud.create_book(db=db, book=book)


@app.get("/books/{author_id}/", response_model=schemas.Book)
def get_books_by_author_id(author_id, db=Depends(get_db)):
    return crud.get_books_by_author_id(db=db, author_id=author_id)
