from fastapi import FastAPI, Depends
from fastapi_crudrouter import SQLAlchemyCRUDRouter
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


author_router = SQLAlchemyCRUDRouter(
    schema=schemas.Author,
    create_schema=schemas.AuthorCreate,
    db_model=models.Author,
    db=get_db,
    prefix="library/authors/",
    delete_all_route=False,
)
app.include_router(author_router)


def get_all(
    author_ids: str | None = None, db: Session = Depends(get_db)
) -> list[models.Book]:
    return crud.get_books_list(db=db, author_ids=author_ids)


book_router = SQLAlchemyCRUDRouter(
    schema=schemas.Book,
    get_all_route=[Depends(get_all)],
    delete_all_route=False,
    create_schema=schemas.BookCreate,
    db_model=models.Book,
    db=get_db,
    prefix="library/books/",
)
app.include_router(book_router)
