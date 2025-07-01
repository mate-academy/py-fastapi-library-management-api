from fastapi import FastAPI, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session

import crud
import schemas
from db.database import get_db

app = FastAPI()


@app.get("/authors/", response_model=schemas.AuthorList)
def author_list(
    page: int = Query(1, ge=1),
    per_page: int = Query(5, le=20),
    db: Session = Depends(get_db),
):
    offset = (page - 1) * per_page

    db_authors = crud.get_author_list(db=db, skip=offset, limit=per_page)
    total_authors = crud.get_author_count(db=db)
    total_pages = (total_authors + per_page - 1) // per_page

    return {
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages,
        "authors": db_authors,
    }


@app.get("/authors/{author_id}", response_model=schemas.Author)
def author_detail(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_id(db=db, author_id=author_id)

    if db_author is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Author not found"
        )

    return db_author


@app.post(
    "/authors/",
    response_model=schemas.Author,
    status_code=status.HTTP_201_CREATED,
)
def author_create(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=schemas.BookList)
def book_list(
    author: int = Query(None, description="Author ID"),
    page: int = Query(1, ge=1),
    per_page: int = Query(5, le=20),
    db: Session = Depends(get_db),
):
    offset = (page - 1) * per_page

    db_books = crud.get_book_list(
        db=db, skip=offset, limit=per_page, author_id=author
    )
    total_books = crud.get_book_count(db=db)
    total_pages = (total_books + per_page - 1) // per_page

    return {
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages,
        "books": db_books,
    }


@app.post(
    "/books/", response_model=schemas.Book, status_code=status.HTTP_201_CREATED
)
def book_create(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)
