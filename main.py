from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def paginate(objects: list[any], skip: int, limit: int) -> list[any] | str:
    amount_of_objects = len(objects)
    if not 0 <= skip < amount_of_objects:
        return (
            "Skip should be greater or equal 0 and less then "
            f"{amount_of_objects}"
        )

    if limit < 1:
        return "Limit should be greater or equal 1"
    return objects[skip : skip + limit]


@app.post("/library/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    if crud.get_author_by_name(db=db, name=author.name):
        raise HTTPException(
            status_code=400, detail="Such Author already exist"
        )

    return crud.create_author(db=db, author=author)


@app.get("/library/authors/", response_model=list[schemas.Author])
def read_authors(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    authors = crud.get_all_author(db=db)
    page = paginate(authors, skip=skip, limit=limit)
    if isinstance(page, str):
        raise HTTPException(status_code=400, detail=page)
    return page


@app.get("/library/authors/{author_id}/", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author(db=db, author_id=author_id)

    if not author:
        raise HTTPException(status_code=400, detail="Author does not exist")

    return author


@app.delete("/library/authors/{author_id}/", status_code=204)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    num_deleted_authors = crud.delete_author(db=db, author_id=author_id)

    if not num_deleted_authors:
        raise HTTPException(status_code=400, detail="Author does not exist")


@app.patch("/library/authors/{author_id}/", response_model=schemas.Author)
def update_author(
    author_id: int, author: schemas.AuthorUpdate, db: Session = Depends(get_db)
):
    db_author = crud.get_author(db=db, author_id=author_id)

    if not db_author:
        raise HTTPException(status_code=400, detail="Author does not exist")

    return crud.update_author(db=db, db_author=db_author, author=author)


@app.post("/library/books/", response_model=schemas.Book)
def create_books(
    book: schemas.BookCreate, db: Session = Depends(get_db)
) -> models.Book:
    if crud.get_book_by_title(db=db, title=book.title):
        raise HTTPException(status_code=400, detail="Such Book already exist")

    return crud.create_book(db=db, book=book)


@app.get("/library/books/", response_model=list[schemas.Book])
def read_books(
    author_ids: str | None = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
) -> list[models.Book]:
    books = crud.get_books_list(db=db, author_ids=author_ids)
    page = paginate(books, skip=skip, limit=limit)
    if isinstance(page, str):
        raise HTTPException(status_code=400, detail=page)
    return page


@app.get("/library/books/{books_id}/", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db=db, book_id=book_id)

    if not book:
        raise HTTPException(status_code=400, detail="Author does not exist")

    return book


@app.patch("/library/books/{book_id}/", response_model=schemas.Author)
def update_book(
    book_id: int, book: schemas.BookUpdate, db: Session = Depends(get_db)
):
    db_book = crud.get_book(db=db, book_id=book_id)

    if not db_book:
        raise HTTPException(status_code=400, detail="Author does not exist")

    return crud.update_book(db=db, db_book=db_book, book=book)


@app.delete("/library/books/{book_id}/", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    num_deleted_books = crud.delete_book(db=db, book_id=book_id)

    if not num_deleted_books:
        raise HTTPException(status_code=400, detail="Book does not exist")
