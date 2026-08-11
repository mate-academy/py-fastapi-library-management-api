from sqlalchemy.orm import Session
from database import SessionLocal
from fastapi import FastAPI, Depends, HTTPException
import schemas, crud

app = FastAPI(
    docs_url="/docx"
)


def get_db() -> Session: # type: ignore
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[schemas.Author])
def get_authors(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
) -> list[schemas.Author]:
    return crud.get_authors(
        db,
        skip=skip,
        limit=limit
    )


@app.get("/authors/{author_id}", response_model=schemas.Author)
def get_authors(
    author_id: int,
    db: Session = Depends(get_db)
) -> schemas.Author:

    author = crud.get_author_by_id(
        db=db,
        author_id=author_id)

    if author:
        return author
    raise HTTPException(
        status_code=404,
        detail="Author not found"
    )


@app.post("/authors/", response_model=schemas.Author)
def create_author(
    author: schemas.AuthorBase,
    db: Session = Depends(get_db)
)-> schemas.Author:
    db_author = crud.get_author_by_name(db=db, name=author.name)
    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Author with this name already exists")
    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=list[schemas.Book])
def get_book(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
)-> list[schemas.Book]:
    return crud.get_books(
        db,
        skip=skip,
        limit=limit
    )


@app.get("/books/{author_id}", response_model=list[schemas.Book])
def get_books(
    author_id: int,
    db: Session = Depends(get_db)
)-> list[schemas.Book]:
    books = crud.get_books_by_author_id(db=db, author_id=author_id)
    if books:
        return books
    raise HTTPException(
        status_code=404,
        detail="No books found"
    )


@app.post("/authors/{author_id}/books", response_model=schemas.Book)
def create_book(
    author_id: int,
    book: schemas.BookBase,
    db: Session = Depends(get_db)
)-> schemas.Book:
    autor = crud.get_books_by_author_id(
        db=db,
        author_id=author_id
    )

    if autor:
        return crud.create_book(
            db=db,
            book=book,
            author_id=author_id
        )
    raise HTTPException(
        status_code=404,
        detail="Author not found",
    )
