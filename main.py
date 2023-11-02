from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from db.database import SessionLocal

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
    return crud.get_all_authors(db)


@app.post("/authors/", response_model=schemas.Author)
def create_authors(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    # db_author = crud.get_author_by_name(db=db, name=author.name)
    #
    # if db_author:
    #     raise HTTPException(status_code=400, detail="Author with")
    return crud.create_author(db=db, author=author)
