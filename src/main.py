"""FastAPI entrypoint."""

from fastapi import FastAPI
from fastapi_pagination import add_pagination

from src.routes import library_router

app = FastAPI(
    title="Library FastApi homework",
    description="Description of project",
)

api_version_prefix = "/api/v1"

app.include_router(
    library_router,
    prefix=f"{api_version_prefix}/library",
    tags=["library"],
)

add_pagination(app)
