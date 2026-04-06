from typing import Annotated, Generator
from fastapi import Depends
from sqlalchemy.orm import Session
import crud
import schemas
from db.database import SessionLocal
from fastapi import FastAPI
from db.database import engine
from db.models import Base


app = FastAPI()
Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/books/", response_model=list[schemas.BookListSchema])
def read_cheese_types(
        db: Annotated[Session, Depends(get_db)],
        author_id: int | None = None,
        skip: int | None = None,
        limit: int | None = None,
):
    return crud.get_all_books(
        db=db,
        author_id=author_id,
        skip=skip,
        limit=limit
    )


@app.post("/books/", response_model=schemas.BookSchemaBase)
def create_book_route(
    book: schemas.BookCreateSchema,
    db: Session = Depends(get_db)
):
    return crud.create_book(db=db, book=book)


@app.get("/authors/", response_model=list[schemas.AuthorListSchema])
def get_authors(
        db: Annotated[Session, Depends(get_db)],
        skip: int | None = None,
        limit: int | None = None,
):
    return crud.get_authors_list(db=db, skip=skip, limit=limit)


@app.post("/authors/", response_model=schemas.AuthorSchema)
def create_author_route(
    author: schemas.AuthorSchemaBase,
    db: Session = Depends(get_db)
):
    return crud.create_author(db=db, author=author)


@app.get("/authors/{author_id}/", response_model=schemas.AuthorListSchema)
def get_authors_by_author_id(
    db: Annotated[Session, Depends(get_db)],
    author_id: int,
):
    return crud.get_author_by_id(
        db=db, author_id=author_id
    )
