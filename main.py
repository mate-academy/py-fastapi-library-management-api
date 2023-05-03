from typing import Union

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

# import crud
# import schemas
# from db.database import SessionLocal
#
app = FastAPI()
#
#
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}
