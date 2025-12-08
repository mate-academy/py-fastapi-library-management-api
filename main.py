from fastapi import FastAPI

from library_service.routes import authors_router, books_router

app = FastAPI()

api_version_prefix = "/api/v1"

app.include_router(authors_router, prefix=f"{api_version_prefix}/authors", tags=["authors"])
app.include_router(books_router, prefix=f"{api_version_prefix}/books", tags=["books"])
