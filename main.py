from typing import List

from fastapi import FastAPI
from sqlalchemy.orm import Session

from schemas import AuthorRead

app = FastAPI()


# @app.get("/authors/", response_model=List[AuthorRead])
# def read_authors(db: Session = Depends(get_db)):
#     return crud.get_all_beer_types(db=db)
