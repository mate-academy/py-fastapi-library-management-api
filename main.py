from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal

import schemas
import crud
app = FastAPI()


@app.get("/")
def hello():
    return "Hello!"


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/books", response_model=list[schemas.Book])
def get_books(db: Session = Depends(get_db)):
    return crud.get_books(db)

