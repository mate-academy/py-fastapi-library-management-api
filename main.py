from fastapi import FastAPI, Depends
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
