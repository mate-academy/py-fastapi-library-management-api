from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

import database
import models
import schemas
import crud

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


@app.get("/authors/", response_model=list[schemas.AuthorRead])
def read_authors(
    skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)
):
    return crud.get_authors(db=db, skip=skip, limit=limit)


@app.post("/authors/", response_model=schemas.AuthorRead)
def create_author(
    author: schemas.AuthorCreate, db: Session = Depends(database.get_db)
):
    db_author = crud.get_author_by_name(db=db, name=author.name)
    if db_author:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Author already exist",
        )
    return crud.create_author(db=db, author=author)


@app.get("/authors/{author_id}/", response_model=schemas.AuthorRead)
def create_author(author_id: int, db: Session = Depends(database.get_db)):
    db_author = crud.get_author_by_id(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Author not found",
        )
    return db_author
