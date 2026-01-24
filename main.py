from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get(
    "/author/",
    response_model=list[schemas.Author],
    tags=["Author"],
)
def get_list_of_author(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
) -> list[schemas.Author]:
    return crud.get_list_authors(db=db, skip=skip, limit=limit)


@app.get(
    "/author/{author_id}/",
    response_model=schemas.Author,
    tags=["Author"],
)
def get_author(
        author_id: int,
        db: Session = Depends(get_db),
) -> schemas.Author:
    return crud.get_author_by_id(db=db, author_id=author_id)


@app.post(
    "/author/",
    response_model=schemas.AuthorCreate,
    tags=["Author"],
)
def create_author(
        author_data: schemas.AuthorCreate,
        db: Session = Depends(get_db),
) -> schemas.Author:
    return crud.create_author(
        db=db,
        author_data=author_data,
    )


@app.put(
    "/author/{author_id}/",
    response_model=schemas.AuthorUpdate,
    tags=["Author"],
)
def update_author(
        author_id: int,
        author_data: schemas.AuthorUpdate,
        db: Session = Depends(get_db),
) -> schemas.Author:
    return crud.update_author(
        db=db,
        author_id=author_id,
        author_data=author_data,
    )


@app.patch(
    "/author/{author_id}/",
    response_model=schemas.AuthorUpdate,
    tags=["Author"],
)
def patch_author(
        author_id: int,
        author_data: schemas.AuthorUpdate,
        db: Session = Depends(get_db),
) -> schemas.Author:
    return crud.update_author(
        db=db,
        author_id=author_id,
        author_data=author_data,
    )


@app.delete(
    "/author/{author_id}/",
    tags=["Author"],
)
def delete_author(
        author_id: int,
        db: Session = Depends(get_db),
) -> schemas.Author:
    return crud.delete_author(
        db=db,
        author_id=author_id,
    )


@app.get(
    "/books/",
    response_model=list[schemas.Book],
    tags=["Book"],
)
def get_list_of_books(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
        author_id: int = None,
) -> list[schemas.Book]:
    return crud.get_list_of_books(
        db=db,
        skip=skip,
        limit=limit,
        author_id=author_id
    )


@app.get(
    "/books/{book_id}/",
    response_model=schemas.Book,
    tags=["Book"],
)
def get_book(
        book_id: int,
        db: Session = Depends(get_db),
) -> schemas.Book:
    return crud.get_book_by_id(db=db, book_id=book_id)


@app.post(
    "/books/",
    response_model=schemas.BookCreate,
    tags=["Book"],
)
def create_book(
        book_data: schemas.BookCreate,
        db: Session = Depends(get_db),
) -> schemas.Book:
    return crud.create_book(
        db=db,
        book_data=book_data,
    )


@app.put(
    "/books/{book_id}/",
    response_model=schemas.BookUpdate,
    tags=["Book"],
)
def update_book(
        book_id: int,
        book_data: schemas.BookUpdate,
        db: Session = Depends(get_db),
) -> schemas.Book:
    return crud.update_book(
        db=db,
        book_id=book_id,
        book_data=book_data,
    )


@app.patch(
    "/books/{book_id}/",
    response_model=schemas.Book,
    tags=["Book"],
)
def patch_book(
        book_id: int,
        book_data: schemas.BookUpdate,
        db: Session = Depends(get_db),
) -> schemas.Book:
    return crud.update_book(
        db=db,
        book_id=book_id,
        book_data=book_data,
    )


@app.delete(
    "/books/{book_id}/",
    tags=["Book"],
)
def delete_book(
        book_id: int,
        db: Session = Depends(get_db),
) -> schemas.Book:
    return crud.delete_book(
        db=db,
        book_id=book_id,
    )
