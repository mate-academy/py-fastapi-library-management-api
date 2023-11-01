from fastapi import FastAPI, Depends, HTTPException
from library_management import crud, schemas, database
import uvicorn

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", tags=["ROOT"])
def root() -> dict:
    return {"message": "Hello, world"}

# create new author
# list of authors with pagination
# detail author
# new book for a specific author
# list of books

@app.get("/books", tags=["books"])
def read_books() -> dict:
    return {"data": "Data from db"}


# filter books


if __name__ == "__main__":
    uvicorn.run(
        "library_management.main:app", port=8000, reload=True
    )