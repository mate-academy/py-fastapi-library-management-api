from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    Query
)
from sqlalchemy.orm import Session

from crud import (
    get_author,
    get_all_authors,
    get_all_books,
    add_book,
    add_author
)

from schemas import (
    Author,
    AuthorCreate,
    BookCreate,
    Book
)

from database import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root() -> dict:
    return {"message": "Hello"}


@app.get("/authors/", response_model=list[Author])
def read_authors(
        db: Session = Depends(get_db),
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1)
) -> dict:
    return get_all_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/", response_model=Author)
def read_single_author(author_id: int, db: Session = Depends(get_db)):
    db_author = get_author(db=db, author_id=author_id)

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.post("/authors/", response_model=Author)
def create_author(
    author: AuthorCreate,
    db: Session = Depends(get_db)
):
    return add_author(db=db, author=author)


@app.get("/books/", response_model=list[Book])
def read_books(
    author_id: int = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db)
):
    return get_all_books(db=db, skip=skip, limit=limit, author_id=author_id)


@app.post("/books/", response_model=Book)
def create_book(
    book: BookCreate,
    db: Session = Depends(get_db)
):
    return add_book(db=db, book=book)
