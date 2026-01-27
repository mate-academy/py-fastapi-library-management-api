from fastapi import FastAPI

from crud_operations import crud


app = FastAPI()

app.include_router(crud.router, tags=["books"])
