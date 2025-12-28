from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal, Base, engine


Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[schemas.Author], status_code=200)
def read_authors(
        db: Session = Depends(get_db),
        skip: int | None = None,
        limit: int | None = None
):
    return crud.get_authors(db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    return crud.get_author(author_id=author_id, db=db)


@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author_schema: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    return crud.create_author(db=db, author_schema=author_schema)


@app.put("/authors/{author_id}", response_model=schemas.Author)
def update_author(
        author_id: int,
        author_schema: schemas.AuthorUpdate,
        db: Session = Depends(get_db)
):
    return crud.update_author(
        author_id=author_id,
        author_schema=author_schema,
        db=db
    )


@app.delete("/authors/{author_id}")
def delete_author(author_id: int, db: Session = Depends(get_db)):
    return crud.delete_author(author_id=author_id, db=db)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
        db: Session = Depends(get_db),
        author_id: int | None = None,
        skip: int | None = None,
        limit: int | None = None
):
    return crud.get_books(db, author_id=author_id, skip=skip, limit=limit)


@app.get("/books/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    return crud.get_book(book_id=book_id, db=db)


@app.post("/books/", response_model=schemas.Book)
def create_book(
        book_schema: schemas.BookCreate,
        db: Session = Depends(get_db)
):
    return crud.create_book(book_schema=book_schema, db=db)


@app.put("/books/{book_id}", response_model=schemas.Book)
def update_book(
        book_id: int,
        book_schema: schemas.BookUpdate,
        db: Session = Depends(get_db)
):
    return crud.update_book(book_id=book_id, book_schema=book_schema, db=db)


@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    return crud.delete_book(book_id=book_id, db=db)
