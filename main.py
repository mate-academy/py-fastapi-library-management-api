from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from database import SessionLocal

import schemas
import crud
app = FastAPI()


@app.get("/")
def hello():
    return "Hello!"


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/authors/", response_model=list[schemas.AuthorList])
def get_list_authors(
        skip: int = Query(0, ge=0),
        limit: int = Query(2, ge=1, le=2),
        db: Session = Depends(get_db)
):
    return crud.get_all_authors(skip=skip, limit=limit, db=db)

@app.get("/books/", response_model=list[schemas.BookList])
def get_list_books(
        skip: int = Query(0, ge=0),
        limit: int = Query(2, ge=1, le=2),
        db: Session = Depends(get_db)):
    return crud.get_all_books(skip=skip, limit=limit, db=db)
