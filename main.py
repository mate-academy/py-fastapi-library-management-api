import uvicorn
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException

import crud
import schemas
from db.database import SessionLocal

app = FastAPI()


def session_manager() -> Session:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@app.get("/")
def root():
    return {"message": "Hello, world"}


@app.post("/author/", response_model=schemas.Author)
def create_author(
        author: schemas.CreateAuthor,
        session: Session = Depends(session_manager)
):
    search_for_author = crud.get_author_by_name(session=session,
                                                author_name=author.name)

    if search_for_author:
        raise HTTPException(
            status_code=400,
            detail="Such author already exists in DB"
        )

    return crud.create_author(session=session,
                              author=author)


@app.get("/author/", response_model=list[schemas.Author])
def read_all_authors(session: Session = Depends(session_manager),
                     skip: int = 0,
                     limit: int = 2):
    search_for_author = crud.get_author_by_id(session=session,
                                              author_id=1, )

    if search_for_author is None:
        raise HTTPException(status_code=404, detail="Data Base is Empty")

    return crud.get_authors_list(session=session,
                                 skip=skip,
                                 limit=limit)


@app.get("/author/{author_id}", response_model=schemas.Author)
def read_single_author(
        author_id: int,
        session: Session = Depends(session_manager)
):
    search_for_author = crud.get_author_by_id(session=session,
                                              author_id=author_id)

    if search_for_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return search_for_author


@app.post("/book/")
def create_book(
        book: schemas.CreateBook,
        session: Session = Depends(session_manager)
):
    search_for_book = crud.get_books_by_name(
        session=session,
        book_title=book.title
    )

    if search_for_book:
        raise HTTPException(
            status_code=400, detail="Such book already exists in DB"
        )

    return crud.create_book(session=session,
                            book=book)


@app.get("/book/", response_model=list[schemas.Book])
def read_all_books(session: Session = Depends(session_manager),
                   skip: int = 0,
                   limit: int = 2):
    search_for_books = crud.get_books_by_id(session=session,
                                            book_id=1)

    if search_for_books is None:
        raise HTTPException(status_code=404,
                            detail="No books added yet")

    return crud.get_books_list(session=session,
                               skip=skip,
                               limit=limit)


@app.get("/author/{author_id}/books/",
         response_model=list[schemas.Book])
def read_single_author_books(
        author_id: int,
        session: Session = Depends(session_manager)
):
    search_for_author = crud.get_author_by_id(session=session,
                                              author_id=author_id)

    if search_for_author is None:
        raise HTTPException(status_code=404,
                            detail="Author not found")

    search_for_author_books = crud.get_books_by_author_id(
        session=session,
        author_id=author_id
    )
    if len(search_for_author_books) == 0:
        raise HTTPException(status_code=404,
                            detail="Books not found")

    return search_for_author_books
