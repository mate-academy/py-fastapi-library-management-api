from fastapi import FastAPI
from app import routes

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to the Library!"}


app.include_router(routes.router)
