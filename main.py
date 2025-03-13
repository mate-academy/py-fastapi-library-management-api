from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from models import Base
from database import engine
from routers import author, book

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)


app.include_router(author.router, prefix="/authors", tags=["authors"])
app.include_router(book.router, prefix="/books", tags=["books"])

@app.get("/", tags=["root"])
async def root():
    return {"message": "Hello World!"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)