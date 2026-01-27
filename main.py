from typing import List

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import crud
from database import SessionLocal
from schemas import AuthorRead

app = FastAPI()

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/authors/", response_model=List[AuthorRead])
def read_authors(db: Session = Depends(get_db)):
    return crud.get_all_authors(db=db)
