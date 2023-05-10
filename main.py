from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

PAGE_SIZE = 10

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.post("/library/authors/", response_model=schemas.Author)
def create_author(
    author: schemas.AuthorCreate, db: Session = Depends(get_db)
) -> models.Author | HTTPException:
    if crud.get_author_by_name(db=db, name=author.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Such Author already exist",
        )

    return crud.create_author(db=db, author=author)


@app.get("/library/authors/", response_model=list[schemas.Author])
def read_authors(
    skip: int = 0,
    limit: int = PAGE_SIZE,
    db: Session = Depends(get_db),
) -> list[models.Author]:
    return crud.get_all_author(db=db, skip=skip, limit=limit)


@app.get("/library/authors/{author_id}/", response_model=schemas.Author)
def read_author(
    author_id: int, db: Session = Depends(get_db)
) -> models.Author:
    author = crud.get_author(db=db, author_id=author_id)

    if not author:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Author does not exist",
        )

    return author


@app.delete(
    "/library/authors/{author_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
def delete_author(
    author_id: int, db: Session = Depends(get_db)
) -> HTTPException | None:
    num_deleted_authors = crud.delete_author(db=db, author_id=author_id)

    if not num_deleted_authors:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Author does not exist",
        )


@app.patch("/library/authors/{author_id}/", response_model=schemas.Author)
def update_author(
    author_id: int, author: schemas.AuthorUpdate, db: Session = Depends(get_db)
) -> models.Author | HTTPException:
    db_author = crud.get_author(db=db, author_id=author_id)

    if not db_author:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Author does not exist",
        )

    return crud.update_author(db=db, db_author=db_author, author=author)


@app.post("/library/books/", response_model=schemas.Book)
def create_books(
    book: schemas.BookCreate, db: Session = Depends(get_db)
) -> models.Book | HTTPException:
    if crud.get_book_by_title(db=db, title=book.title):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Such Book already exist",
        )

    return crud.create_book(db=db, book=book)


@app.get("/library/books/", response_model=list[schemas.Book])
def read_books(
    author_ids: str | None = None,
    skip: int = 0,
    limit: int = PAGE_SIZE,
    db: Session = Depends(get_db),
) -> list[models.Book]:
    return crud.get_books_list(
        db=db, author_ids=author_ids, skip=skip, limit=limit
    )


@app.get("/library/books/{books_id}/", response_model=schemas.Book)
def read_book(
    book_id: int, db: Session = Depends(get_db)
) -> models.Book | HTTPException:
    book = crud.get_book(db=db, book_id=book_id)

    if not book:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Author does not exist",
        )

    return book


@app.patch("/library/books/{book_id}/", response_model=schemas.Author)
def update_book(
    book_id: int, book: schemas.BookUpdate, db: Session = Depends(get_db)
) -> models.Book | HTTPException:
    db_book = crud.get_book(db=db, book_id=book_id)

    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Author does not exist",
        )

    return crud.update_book(db=db, db_book=db_book, book=book)


@app.delete(
    "/library/books/{book_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
def delete_book(
    book_id: int, db: Session = Depends(get_db)
) -> HTTPException | None:
    num_deleted_books = crud.delete_book(db=db, book_id=book_id)

    if not num_deleted_books:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book does not exist",
        )
    return
