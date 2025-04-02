from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy.orm import Session

import crud
from db.database import SessionLocal
from schemas import AuthorList, AuthorRetrieve, AuthorCreate, BookList, BookRetrieve, BookCreate

app = FastAPI()

def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/authors/", response_model=AuthorList)
def get_authors(
        page: int = Query(1, ge=1),
        per_page: int = Query(10, ge=1, le=20),
        db: Session = Depends(get_db),
):
    total_items = crud.get_total_authors_count(db)
    if total_items == 0:
        raise HTTPException(status_code=404, detail="No authors found.")

    total_pages = (total_items + per_page -1) // per_page
    authors = crud.get_authors(db, skip=(page - 1) * per_page, limit=per_page)

    prev_page = f"/authors/?page={page-1}&per_page={per_page}" if page > 1 else None
    next_page = f"/authors/?page={page+1}&per_page={per_page}" if page < total_pages else None

    return AuthorList(
        authors=authors,
        total_items=total_items,
        total_pages=total_pages,
        prev_page=prev_page,
        next_page=next_page
    )

@app.get("/authors/{author_id}", response_model=AuthorRetrieve)
def get_one_author(
        author_id: int,
        db: Session = Depends(get_db)
):
    author = crud.get_one_author(author_id=author_id, db=db)
    if not author:
        raise HTTPException(status_code=404, detail="Author with the given ID was not found.")
    return AuthorRetrieve.model_validate(author)


@app.post("/authors/", response_model=AuthorCreate)
def create_author(
        author: AuthorCreate,
        db: Session = Depends(get_db)
):
    db_author = crud.get_author_by_name(db=db, name=author.name)
    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Author with such title is already exist."
        )

    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=BookList)
def get_books(
        page: int = Query(1, ge=1),
        per_page: int = Query(10, ge=1, le=20),
        author_id: int | None = None,
        db: Session = Depends(get_db),
):
    total_items = crud.get_total_books_count(db)
    if total_items == 0:
        raise HTTPException(status_code=404, detail="No books found.")

    total_pages = (total_items + per_page -1) // per_page

    books = crud.get_books(
        db=db,
        skip=(page - 1) * per_page,
        limit=per_page,
        author_id=author_id)

    prev_page = f"/books/?page={page-1}&per_page={per_page}" if page > 1 else None
    next_page = f"/books/?page={page+1}&per_page={per_page}" if page < total_pages else None

    return BookList(
        books=books,
        total_items=total_items,
        total_pages=total_pages,
        prev_page=prev_page,
        next_page=next_page
    )

@app.get("/books/{book_id}", response_model=BookRetrieve)
def get_one_book(
        book_id: int,
        db: Session = Depends(get_db)
):
    book = crud.get_one_book(book_id=book_id, db=db)
    if not book:
        raise HTTPException(status_code=404, detail="Books with the given ID was not found.")

    return BookRetrieve.model_validate(book)

@app.post("/books/", response_model=BookCreate)
def create_book(
        book: BookCreate,
        db: Session = Depends(get_db)
):
    db_book = crud.get_book_by_title(db=db, title=book.title)

    if db_book:
        raise HTTPException(
            status_code=400,
            detail="Book with such name is already exist."
        )

    return crud.create_book(db=db, book=book)

