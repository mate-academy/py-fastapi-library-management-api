from typing import Generator, Annotated
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import crud
import schemas
from db.engine import SessionLocal

app = FastAPI(title="Library API")


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=List[schemas.Author])
def read_authors(
    db: Annotated[Session, Depends(get_db)], skip: int = 0, limit: int = 10
):
    return crud.get_all_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Annotated[Session, Depends(get_db)]):
    db_author = crud.get_author_by_id(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_name(db, name=author.name)
    if db_author:
        raise HTTPException(status_code=400, detail="Author already registered")
    return crud.create_author(db=db, author=author)
