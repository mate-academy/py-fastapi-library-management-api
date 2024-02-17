from fastapi import FastAPI

from library.routers import router

app = FastAPI()

app.include_router(router)
