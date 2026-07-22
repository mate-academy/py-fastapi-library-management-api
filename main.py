from fastapi import FastAPI, HTTPException, Query
from sqlalchemy.exc import IntegrityError

import crud
from database import Base, SessionDep, engine
from schemas import (
    AuthorCreateSchema,
    AuthorSchema,
    BookCreateSchema,
    BookSchema,
    PaginatedAuthorsSchema,
    PaginatedBooksSchema,
)

Base.metadata.create_all(engine)
app = FastAPI()


@app.get("/authors/")
def get_all_authors(
    session: SessionDep,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
) -> PaginatedAuthorsSchema:
    authors = crud.get_all_authors(session, skip=skip, limit=limit)
    total = crud.count_authors(session=session)
    return PaginatedAuthorsSchema(
        items=[AuthorSchema.model_validate(author) for author in authors],
        total=total,
        skip=skip,
        limit=limit,
    )


@app.get("/authors/{author_id}/")
def get_author(author_id: int, session: SessionDep) -> AuthorSchema:
    author = crud.get_author_by_id(session=session, author_id=author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return AuthorSchema.model_validate(author)


@app.post("/authors/")
def add_author(author_data: AuthorCreateSchema, session: SessionDep) -> AuthorSchema:
    try:
        author = crud.create_author(session=session, data=author_data)
    except IntegrityError:
        raise HTTPException(
            status_code=400, detail="Author with this name already exists"
        )
    return AuthorSchema.model_validate(author)


@app.post("/books/")
def add_book(book_data: BookCreateSchema, session: SessionDep) -> BookSchema:
    book = crud.create_book(session=session, data=book_data)
    return BookSchema.model_validate(book)


@app.get("/books/")
def get_all_books(
    session: SessionDep,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    author_id: int | None = Query(None, alias="author_id"),
) -> PaginatedBooksSchema:
    books = crud.get_all_books(session, skip=skip, limit=limit, author_id=author_id)
    total = crud.count_books(session=session, author_id=author_id)
    return PaginatedBooksSchema(
        items=[BookSchema.model_validate(book) for book in books],
        total=total,
        skip=skip,
        limit=limit,
    )
