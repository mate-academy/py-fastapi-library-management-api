from fastapi import FastAPI, Query, Depends, HTTPException
from sqlalchemy.orm import Session

import schemas
import crud
from db.engine import SessionLocal

app = FastAPI()


def get_db_session():
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/authors/", response_model=list[schemas.Author])
def list_authors(
        page: int = Query(1, description="Page number", gt=0),
        page_size: int = Query(
            10,
            description="Number of items per page",
            gt=0
        ),
        db_session: Session = Depends(get_db_session),
):
    authors = crud.get_authors_list(
        db_session=db_session,
        page=page,
        page_size=page_size
    )
    return authors


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def author_detail(
        author_id: int,
        db_session: Session = Depends(get_db_session)
):
    db_author = crud.get_author_detail(
        db_session=db_session,
        author_id=author_id
    )
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author_schema_data: schemas.AuthorCreate,
        db_session: Session = Depends(get_db_session)
):
    db_author = crud.get_author_by_name(
        db_session=db_session,
        name=author_schema_data.name
    )

    if db_author is not None:
        raise HTTPException(
            status_code=400,
            detail="Such author name already exists"
        )

    return crud.create_author(
        db_session=db_session,
        author_schema_data=author_schema_data
    )


@app.get("/books/", response_model=list[schemas.Book])
def list_books(
        page: int = Query(1, description="Page number", gt=0),
        page_size: int = Query(
            10,
            description="Number of items per page",
            gt=0
        ),
        author_id: int | None = None,
        db_session: Session = Depends(get_db_session),
):
    return crud.get_books_list(
        db_session=db_session,
        page=page,
        page_size=page_size,
        author_id=author_id
    )


@app.post("/books/", response_model=schemas.Book)
def create_book(
        book_schema_data: schemas.BookCreate,
        db_session: Session = Depends(get_db_session)
):
    db_book = crud.get_book_by_title(
        db_session=db_session,
        title=book_schema_data.title
    )

    if db_book is not None:
        raise HTTPException(
            status_code=400,
            detail="Such book title already exists"
        )

    return crud.create_book(
        db_session=db_session,
        book_schema_data=book_schema_data
    )
