from fastapi import FastAPI, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from library_api import crud
from library_api.db.engine import SessionLocal
from library_api.schemas import Author, AuthorCreate, BookCreate, Book

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[Author])
def read_authors(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    authors = crud.get_all_authors(db, skip=skip, limit=limit)
    return authors


@app.get("/authors/{id}", response_model=Author)
def read_author_by_id(id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_id(db=db, id=id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.post("/authors/", response_model=Author)
def create_authors(author: AuthorCreate, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_name(db=db, name=author.name)
    if db_author:
        raise HTTPException(status_code=400, detail="Author already exists")
    crud.create_author(db=db, author=author)
    return Response(status_code=200, content="Author created")


@app.get("/books/", response_model=list[Book])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = crud.get_all_books(db, skip=skip, limit=limit)
    return books


@app.get("/books/{id}", response_model=Book)
def read_book_by_id(id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book_by_id(db=db, id=id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@app.get("/authors/{author_id}/books/", response_model=list[Book])
def read_books_by_author_id(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_id(db=db, id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.get_books_by_author_id(db=db, author_id=author_id)


@app.post("/books/", response_model=Book)
def create_book(book: BookCreate, db: SessionLocal = Depends(get_db)):
    crud.create_book(db=db, book=book)
    return Response(
        status_code=200,
        content="Book created",
    )


@app.get("/books/filter/author/", response_model=list[Book])
def read_books_by_author_name(author_name: str, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_name(db=db, name=author_name)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.get_books_by_author_id(db=db, author_id=db_author.id)


@app.post("/authors/{author_id}/books/", response_model=Book)
def create_book_for_author(
    author_id: int, book: BookCreate, db: Session = Depends(get_db)
):
    db_author = crud.get_author_by_id(db=db, id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    crud.create_book(db=db, book=book)
    return Response(
        status_code=200,
        content=f"Book created for author {author_id}",
    )


@app.delete("/books/{id}")
def delete_book(id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book_by_id(db=db, id=id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    crud.delete_book(db=db, id=id)
    return Response(status_code=204, content="Book deleted")


@app.delete("/authors/{author_id}")
def delete_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_id(db=db, id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    crud.delete_author(db=db, author_id=author_id)
    return Response(status_code=204, content="Author deleted")
