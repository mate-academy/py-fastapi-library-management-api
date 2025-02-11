from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from db.engine import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "Welcome to Library on FastAPI"}


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    authors = crud.get_authors_with_pagination(db=db, skip=skip, limit=limit)
    return authors


@app.get("/authors/{author_id}", response_model=schemas.Author)
def get_author_by_id(
        author_id: int,
        db: Session = Depends(get_db)
):

    author = crud.get_author_by_id(db=db, author_id=author_id)
    if not author:
        raise HTTPException(
            status_code=404,
            detail=f"Author with ID {author_id} not found"
        )
    return author


@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):

    author_by_name = crud.get_author_by_name(db=db, name=author.name)
    print(author_by_name)
    if author_by_name:
        raise HTTPException(
            status_code=409,
            detail=f"Author with name {author.name} already exists"
        )
    else:
        return crud.create_author(db=db, author=author)


@app.put("/authors/{author_id}", response_model=schemas.Author)
def update_author_by_id(
        author_id: int,
        updated_author: schemas.AuthorUpdate,
        db: Session = Depends(get_db),
):

    author = crud.get_author_by_id(db=db, author_id=author_id)
    if not author:
        raise HTTPException(
            status_code=404,
            detail=f"Author with ID {author_id} not found",
        )

    updated_author = crud.update_author(db=db, author_id=author_id, updated_author=updated_author)
    return updated_author


@app.delete("/authors/{author_id}", status_code=204)
def delete_author_by_id(
        author_id: int,
        db: Session = Depends(get_db)
):
    author = crud.get_author_by_id(db=db, author_id=author_id)
    if not author:
        raise HTTPException(
            status_code=404,
            detail=f"Author with ID {author_id} not found"
        )

    db.delete(author)
    db.commit()

    return {"message": f"Author with ID {author_id} was deleted successfully"}


@app.get("/books/", response_model=list[schemas.Book])
def get_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):

    books = crud.get_books_with_pagination(db=db, skip=skip, limit=limit)
    return books


@app.get("/books/by-author/{author_id}", response_model=list[schemas.Book])
def get_books_by_author(
        author_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):

    if not crud.get_author_by_id(db=db, author_id=author_id):
        raise HTTPException(
            status_code=404,
            detail=f"Author with ID {author_id} not found"
        )

    books = crud.get_books_by_author(db=db, author_id=author_id, skip=skip, limit=limit)

    if not books:
        raise HTTPException(
            status_code=200,
            detail=f"This author(id: {author_id}) does not have any books now"
        )

    return books


@app.get("/books/{book_id}", response_model=schemas.Book)
def get_book_by_id(
        book_id: int,
        db: Session = Depends(get_db)
):

    book_id = crud.get_book_by_id(db=db, book_id=book_id)
    if not book_id:
        raise HTTPException(
            status_code=404,
            detail=f"Book with ID {book_id} not found"
        )
    return book_id


@app.post("/books/", response_model=schemas.Book)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
):
    return crud.create_book(db=db, book=book)


@app.put("/books/{book_id}", response_model=schemas.Book)
def update_book_by_id(
        book_id: int,
        updated_book: schemas.BookUpdate,
        db: Session = Depends(get_db),
):

    book = crud.get_book_by_id(db=db, book_id=book_id)
    if not book:
        raise HTTPException(
            status_code=404,
            detail=f"Book with ID {book} not found",
        )

    updated_book = crud.update_book(db=db, book_id=book_id, updated_book=updated_book)
    return updated_book


@app.delete("/books/{book_id}", status_code=204)
def delete_book_by_id(
        book_id: int,
        db: Session = Depends(get_db)
):
    book = crud.get_book_by_id(db=db, book_id=book_id)
    if not book:
        raise HTTPException(
            status_code=404,
            detail=f"Bokk with ID {book_id} not found"
        )

    db.delete(book)
    db.commit()

    return {"message": f"Book with ID {book_id} was deleted successfully"}
