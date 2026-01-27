from fastapi import FastAPI

from crud_operations import book_api, author_api


app = FastAPI()

app.include_router(book_api.router, tags=["books"])
app.include_router(author_api.router, tags=["authors"])
