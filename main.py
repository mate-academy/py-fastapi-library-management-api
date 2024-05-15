from schemas import Author, Book, AuthorCreate, BookCreate
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from crud import AuthorDBManager, BookDBManager
from database import SessionLocal

app = FastAPI()


def get_db() -> Session:
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()


@app.get("/authors/", response_model=list[Author])
async def retrieve_a_list_of_authors(skip: int = 0, limit: int = 20, session=Depends(get_db)):
    manager = AuthorDBManager(session)
    return manager.get_all_items(skip, limit)


@app.get("/authors/{author_id}", response_model=Author)
async def retrieve_a_single_author(author_id, session=Depends(get_db)):
    manager = AuthorDBManager(session)
    return manager.get_single_item_by_id(author_id)


@app.post("/authors/", response_model=Author)
async def create_a_new_author(author: AuthorCreate, session=Depends(get_db)):
    manager = AuthorDBManager(session)
    return manager.create_new_item(item=author)


@app.post("/books/", response_model=Book)
async def create_a_new_book(book: BookCreate, session=Depends(get_db)):
    manager = BookDBManager(session)
    return manager.create_new_item(item=book)


@app.get("/books/", response_model=list[Book])
async def retrieve_a_list_of_books(author_id=None, skip: int = 0, limit: int = 20, session=Depends(get_db)):
    manager = BookDBManager(session)
    return manager.get_all_items(author_id, skip, limit)
