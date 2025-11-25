from fastapi import FastAPI
from routers import books, author


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(books.router)
app.include_router(author.router)