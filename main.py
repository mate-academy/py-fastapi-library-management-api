from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import Base, engine, SessionLocal
import crud
import schemas

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library Management API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/authors", response_model=schemas.AuthorRead, status_code=201)
def create_author(author_in: schemas.AuthorCreate, db: Session = Depends(get_db)):
    # name must be unique
    existing = crud.get_author_by_name(db, author_in.name)
    if existing:
        raise HTTPException(status_code=400, detail="Author with this name already exists.")
    return crud.create_author(db, author_in)


@app.get("/authors", response_model=list[schemas.AuthorRead])
def list_authors(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return crud.get_authors(db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=schemas.AuthorRead)
def get_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author(db, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found.")
    return author


@app.post("/authors/{author_id}/books", response_model=schemas.BookRead, status_code=201)
def create_book_for_author(author_id: int, book_in: schemas.BookCreate, db: Session = Depends(get_db)):
    author = crud.get_author(db, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found.")
    return crud.create_book_for_author(db, author_id, book_in)


@app.get("/books", response_model=list[schemas.BookRead])
def list_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    author_id: int | None = Query(None, ge=1),  # filter by author
    db: Session = Depends(get_db),
):
    return crud.get_books(db, skip=skip, limit=limit, author_id=author_id)
