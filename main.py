from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ⬇️ --- AUTHORS CRUD --- ⬇️


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(page: int = 0, page_size: int = 100, db: Session = Depends(get_db)):
    db_authors = crud.get_authors(db=db, page=page, page_size=page_size)

    return db_authors


@app.post("/authors/", response_model=schemas.Author)
def create_author(
    author_to_create: schemas.AuthorCreateUpdate, db: Session = Depends(get_db)
):
    db_author = crud.get_author_by_name(db=db, author_name=author_to_create.name)

    if db_author is not None:
        raise HTTPException(
            status_code=400, detail="Such name for Author already exists"
        )

    return crud.create_author(db=db, author=author_to_create)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def get_detailed_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_detailed_author(db=db, author_id=author_id)

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.put("/authors/{author_id}/", response_model=schemas.Author)
def update_author(
    author_id_to_update: int,
    author_update_data: schemas.AuthorCreateUpdate,
    db: Session = Depends(get_db),
):
    is_author_exists = bool(
        crud.get_author_by_name(db=db, author_name=author_update_data.name)
    )

    if is_author_exists:
        raise HTTPException(
            status_code=400, detail="Such name for Author already exists"
        )

    db_author = crud.get_detailed_author(db=db, author_id=author_id_to_update)

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return crud.update_author(
        db=db,
        author_id_to_update=author_id_to_update,
        author_update_data=author_update_data,
    )


@app.delete("/authors/{author_id}/", response_model=schemas.Author)
def delete_author(author_id_to_delete: int, db: Session = Depends(get_db)):
    db_author = crud.get_detailed_author(db=db, author_id=author_id_to_delete)

    if db_author is None:
        raise HTTPException(status_code=400, detail="Could not find author to delete")

    return crud.delete_author(db=db, author_id_to_delete=author_id_to_delete)


# ⬇️ --- BOOKS CRUD --- ⬇️


@app.post("/books/", response_model=schemas.Book)
def create_book(
    book_to_create: schemas.BookCreateUpdate, db: Session = Depends(get_db)
):
    db_book = crud.create_book(db=db, book_to_create=book_to_create)

    return db_book


@app.get("/books/", response_model=list[schemas.Book])
def get_books(page: int = 0, page_size: int = 100, db: Session = Depends(get_db)):
    db_books = crud.get_books(db=db, page=page, page_size=page_size)

    return db_books


@app.get("/books/{book_id}/", response_model=schemas.Book)
def get_detailed_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_detailed_book(db=db, book_id=book_id)

    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return db_book


@app.put("/books/{book_id}/", response_model=schemas.Book)
def update_book(
    book_id_to_update: int,
    book_update_data: schemas.BookCreateUpdate,
    db: Session = Depends(get_db),
):
    db_book = crud.get_detailed_book(db=db, book_id=book_id_to_update)

    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return crud.update_book(
        db=db, book_id_to_update=book_id_to_update, book_update_data=book_update_data
    )


@app.delete("/books/{book_id}/", response_model=schemas.Book)
def delete_book(book_id_to_delete: int, db: Session = Depends(get_db)):
    db_book = crud.get_detailed_book(db=db, book_id=book_id_to_delete)

    if db_book is None:
        raise HTTPException(status_code=400, detail="Could not find book to delete")

    return crud.delete_book(db=db, book_id=book_id_to_delete)
