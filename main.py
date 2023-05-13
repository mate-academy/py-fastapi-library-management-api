from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import crud
from database import SessionLocal
from schemas import Author

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Hello world"}


@app.get("/authors", response_model=list[Author])
def read_authors(db: Session = Depends(get_db)):
    return crud.get_authors(db)
