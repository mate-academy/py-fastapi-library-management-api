from fastapi import APIRouter, FastAPI
from fastapi_pagination import add_pagination

from crud import library_router

app = FastAPI()
add_pagination(app)
internal_router = APIRouter()
internal_router.include_router(library_router, prefix="/library")
app.include_router(internal_router)
