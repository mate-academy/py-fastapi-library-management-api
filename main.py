from fastapi import FastAPI
from routers import books, author
from db import models, database


app = FastAPI()
models.Base.metadata.create_all(bind=database.engine)

@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(books.router)
app.include_router(author.router)