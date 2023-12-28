from fastapi import Depends, FastAPI, HTTPException, Query, Request, status
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

import crud
import schemas
from database import SessionLocal
from validators import unique_constraint_handler


app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.exception_handler(ValueError)
def handle_unique_constraint_error(request: Request, exc: ValueError):
    error = exc.errors()[-1]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"field": error["loc"][-1], "message": error["msg"]},
    )


@app.get("/authors/", response_model=list[schemas.Author])
def read_author_list(db: Session = Depends(get_db),
                     skip: int = Query(0, ge=0),
                     limit: int = Query(5)):
    return crud.get_author_list(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_author(db: Session = Depends(get_db), author_id: int | None = None):
    author = crud.get_author_by_id(db=db, author_id=author_id)

    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Author with id {author_id} not found",
        )

    return author


@app.post("/authors/",
          response_model=schemas.Author,
          status_code=status.HTTP_201_CREATED,
          responses={422: {"model": schemas.ValidationErrorResponse,
                           "description": "Validation Error"}})
@unique_constraint_handler
def create_author(db: Session = Depends(get_db), author: schemas.AuthorCreate | None = None):
    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=list[schemas.BookBase])
def read_book_list(db: Session = Depends(get_db),
                   author_id: int = None,
                   skip: int = Query(0, ge=0),
                   limit: int = Query(5)):

    filtered_books = crud.filter_book_by_author_id(
        author_id=author_id, db=db
    )

    if not list(filtered_books):
        return crud.get_book_list(db=db, skip=skip, limit=limit)

    return filtered_books


@app.post("/books/",
          response_model=schemas.Book,
          status_code=status.HTTP_201_CREATED,
          responses={422: {"model": schemas.ValidationErrorResponse,
                          "description": "Validation Error"}})
@unique_constraint_handler
def create_book(db: Session = Depends(get_db), book: schemas.BookCreate | None = None):
    return crud.create_book(db=db, book=book)
