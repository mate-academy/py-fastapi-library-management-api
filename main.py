import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from db import models
import schemas
from db.engine import SessionLocal
import crud

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "FastAPI"}


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(db: Session = Depends(get_db)):
    return crud.get_all_authors(db)


@app.post("/authors/create/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    db_author = crud.create_author(db=db, author=author)
    print("c")
    return db_author

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
