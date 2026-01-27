from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing_extensions import Annotated

import crud
import schemas
from database import SessionLocal
from schemas import AuthorRead, BookRead

app = FastAPI()

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/authors/", response_model=List[AuthorRead])
def read_authors(db: Session = Depends(get_db)):
    return crud.get_all_authors(db=db)


@app.post("/authors/", response_model=schemas.AuthorBase)
def create_author(
        new_author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    db_author = crud.get_author_by_name(db=db, name=new_author.name)

    if db_author:
        raise HTTPException(status_code=400, detail="author name already exist")

    return crud.create_author(db=db, author=new_author)


@app.get("/authors/{id}", response_model=schemas.AuthorRead)
def read_single_author(
    author_id: int,
    db: Annotated[Session, Depends(get_db)]
):
    db_author = crud.get_author_by_id(db=db, author_id=author_id)

    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author

@app.get("/books/", response_model=List[BookRead])
def read_books(db: Session = Depends(get_db)):
    return crud.get_all_books(db=db)