from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from db_library.database import SessionLocal
from db_library.database import Base, engine

import crud
import schemas

app = FastAPI()
Base.metadata.create_all(bind=engine)


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/author/", response_model=list[schemas.Author])
def get_author_all(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
):
    return crud.get_all_authors(db=db, limit=limit, skip=skip)


@app.get("/author/{author_id}/", response_model=schemas.Author)
def get_author_id(
        author: int,
        db: Session = Depends(get_db),
):
    return crud.get_author_by_id(db=db, author=author)


@app.post("/author/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    db_author = crud.get_author_name(db=db, name=author.name)

    if db_author:
        raise HTTPException(
            status_code=400, detail="Author already exists"
        )
    return crud.create_author(db=db, author=author)


@app.get("/book/", response_model=list[schemas.Book])
def get_books(
        author_id: int | None = None,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
):
    return crud.get_books(db=db, author_id=author_id, skip=skip, limit=limit)


@app.post("/author/{author_id}/book/", response_model=schemas.Book)
def create_book(
        book: schemas.BookCreate,
        author_id: int,
        db: Session = Depends(get_db),
):
    return crud.create_book(db=db, book=book, author_id=author_id)
