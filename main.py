from fastapi import FastAPI

from routers.books_routers import books_router
from routers.author_routers import author_router

app = FastAPI()

app.include_router(author_router)
app.include_router(books_router)
