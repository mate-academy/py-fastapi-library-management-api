from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm.session import Session

from library_app.database import get_db
from library_app import schemas, crud

app = FastAPI()


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 5,
):
    return crud.get_authors_list(db=db, skip=skip, limit=limit)


@app.get("/author/{author_id}", response_model=schemas.Author)
def get_author(
        author_id: int,
        db: Session = Depends(get_db),
):
    db_author = crud.get_author_by_id(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.post("/author/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db),
):
    db_author = crud.get_author_by_name(db=db, name=author.name)

    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Author with this name already exists"
        )
    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
        db: Session = Depends(get_db),
        author_id: int | None = None,
        skip: int = 0,
        limit: int = 5,
):
    db_books = crud.get_books_list(
        db=db,
        skip=skip,
        limit=limit,
        author_id=author_id
    )

    if not db_books:
        raise HTTPException(status_code=404, detail="Books not found")
    return db_books


@app.post("/book/", response_model=schemas.Book)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db),
):
    return crud.create_book(db=db, book=book)
