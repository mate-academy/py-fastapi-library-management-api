from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root() -> dict:
    return {"message": "Hello World"}


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(db: Session = Depends(get_db)):
    return crud.get_all_authors(db=db)


@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    return crud.create_author(db=db, author=author)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_author(
        author_id: int,
        db: Session = Depends(get_db)
):
    return crud.get_detail_author(db=db, author_id=author_id)

