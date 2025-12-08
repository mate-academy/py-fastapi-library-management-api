from fastapi import FastAPI

from library_service.author_routes import router as authors_router
from library_service.book_routes import router as books_router
from contextlib import asynccontextmanager

from library_service.database import engine
from library_service.models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
app = FastAPI()

api_version_prefix = "/api/v1"

app.include_router(authors_router, prefix=f"{api_version_prefix}/authors", tags=["authors"])
app.include_router(books_router, prefix=f"{api_version_prefix}/books", tags=["books"])
