from fastapi import FastAPI, Depends, HTTPException
from fastapi_pagination import paginate, add_pagination, Page
from sqlalchemy.orm import Session

import crud
import pagination
import schemas
from database import SessionLocal


app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/books/", response_model=Page[pagination.BookOut])
def get_books_list(
        author_id: int | None = None,
        db: Session = Depends(get_db)
):
    return paginate(crud.get_books(author_id=author_id, db=db))


@app.post("/books/", response_model=schemas.BookRead)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    if crud.get_book_by_title(db, book.title):
        raise HTTPException(
            status_code=400,
            detail="Book with that title already exists",
        )

    return crud.create_book(db=db, book=book)


@app.get("/authors/", response_model=Page[pagination.AuthorOut])
def get_authors_list(db: Session = Depends(get_db)):
    return paginate(crud.get_authors(db))


@app.get("/authors/{author_id}/", response_model=schemas.AuthorReadDetail)
def get_author_detail(author_id: int, db: Session = Depends(get_db)):
    if author := crud.get_author_by_id(db=db, author_id=author_id):
        return author

    raise HTTPException(
        status_code=404,
        detail="Author not found",
    )


@app.post(
    "/authors/{author_id}/create-book/",
    response_model=schemas.AuthorReadDetail
)
def create_book_for_author(
        author_id: int,
        book: schemas.BookAuthorCreate,
        db: Session = Depends(get_db)
):
    if author := crud.get_author_by_id(db, author_id):

        if crud.get_book_by_title(book.title, db):
            raise HTTPException(
                status_code=400,
                detail="Book with that title already exists",
            )

        book_data = book.dict()
        book = schemas.BookCreate(**book_data, author_id=author_id)

        crud.create_book(db, book)
        return author

    raise HTTPException(status_code=404, detail="Author not found")


add_pagination(app)
