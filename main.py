from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
)
from sqlalchemy.orm import Session

import crud
from db.engine import SessionLocal
from schems import (
    Author,
    AuthorCreate,
    Book,
    BookCreate,
)

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[Author])
def get_authors(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
) -> list[Author]:
    return crud.get_authors_with_pagination(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/", response_model=Author)
def get_author_by_id(
        author_id: int,
        db: Session = Depends(get_db)
) -> Author:
    db_author = crud.get_author_by_id(db=db, author_id=author_id)
    if db_author:
        return db_author
    raise HTTPException(
        status_code=404,
        detail="Author not found"
    )


@app.post("/authors/", response_model=Author)
def create_author(
        author: AuthorCreate,
        db: Session = Depends(get_db),

) -> Author:
    db_author = crud.get_author_by_name(db=db, name=author.name)
    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Author with this name already exists"
        )
    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=list[Book])
def get_books(
        skip: int = 0,
        limit: int = 10,
        author_id: int | None = None,
        db: Session = Depends(get_db)
) -> list[Book]:
    return crud.get_books_with_pagination(
        db=db,
        skip=skip,
        limit=limit,
        author_id=author_id
    )


@app.post("/books/", response_model=Book)
def create_book(
        book: BookCreate,
        db: Session = Depends(get_db),
) -> Book:
    db_author = crud.get_author_by_id(db=db, author_id=book.author_id)
    if not db_author:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )
    return crud.create_book(db=db, book=book)
