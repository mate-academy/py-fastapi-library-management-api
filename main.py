from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

import crud
import schemas
from database import SessionLocal

app = FastAPI(
    title="Library Management API",
    description="API для управління авторами та книгами в бібліотеці.",
    version="1.0.0",
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/books", response_model=list[schemas.BookRead])
def read_books_endpoint(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
        author_id: int | None = None
):
    return crud.get_all_books(db, author_id, skip, limit)


@app.post(
    "/books",
    response_model=schemas.BookRead,
    status_code=status.HTTP_201_CREATED,
)
def create_book_endpoint(
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
):
    try:
        return crud.create_book_for_author(db, book)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Несподівана помилка сервера: {e}"
        )


@app.get("/authors", response_model=list[schemas.AuthorRead])
def read_authors_endpoint(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100
):
    return crud.get_all_authors(db, skip, limit)


@app.post(
    "/authors",
    response_model=schemas.AuthorRead,
    status_code=status.HTTP_201_CREATED,
)
def create_author_endpoint(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    try:
        return crud.create_author(db, author)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Несподівана помилка сервера: {e}"
        )


@app.get(
    "/authors/{author_id}",
    response_model=schemas.AuthorRead,
)
def read_author_endpoint(
        author_id: int,
        db: Session = Depends(get_db),
):
    db_author = crud.get_author_by_id(db, author_id)

    if db_author is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Автор не знайдений"
        )
    return db_author
