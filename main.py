from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database.engine import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/authors/", response_model=list[schemas.Author])
def read_author(db: Session = Depends(get_db)):
    return crud.read_all_authors(db)


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_name(db=db, name=author.name)
    if db_author:
        raise HTTPException(
            status_code=400, detail="Such name for Author already exists"
        )
    return crud.create_author(db=db, author=author)


@app.put("/authors/{author_id}", response_model=schemas.Author)
def update_author(
    author_id: int,
    author_update: schemas.AuthorUpdate,
    db: Session = Depends(get_db),
):
    return crud.update_author(db=db, author_id=author_id, author=author_update)
