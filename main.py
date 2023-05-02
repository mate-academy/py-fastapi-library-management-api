from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import engine, SessionLocal

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/authors/", response_model=schemas.AuthorCreate)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    author_name = crud.get_autor_by_name(db=db, autor_name=author.name)
    if author_name:
        raise HTTPException(status_code=400, detail="This name already exists")
    return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=list[schemas.AuthorMain])
def read_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    authors = crud.get_author_list(db=db, skip=skip, limit=limit)
    return authors
