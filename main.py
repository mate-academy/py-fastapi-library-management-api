from schemas import Author, Book, AuthorCreate, BookCreate
from fastapi import FastAPI, Depends
from crud import AuthorDBManager, BookDBManager


app = FastAPI()


def get_author_manager():
    return AuthorDBManager()


def get_book_manager():
    return BookDBManager()


@app.get("/authors/", response_model=list[Author])
async def retrieve_a_list_of_authors(skip: int = 0, limit: int = 20, manager=Depends(get_author_manager)):
    return manager.get_all_items(skip, limit)


@app.get("/authors/{author_id}", response_model=Author)
async def retrieve_a_single_author(author_id, manager=Depends(get_author_manager)):
    return manager.get_single_item_by_id(author_id)


@app.post("/authors/", response_model=Author)
async def create_a_new_author(author: AuthorCreate, manager=Depends(get_author_manager)):
    return manager.create_new_item(item=author)


@app.post("/books/", response_model=Book)
async def create_a_new_book(book: BookCreate, manager=Depends(get_book_manager)):
    return manager.create_new_item(item=book)


@app.get("/books/", response_model=list[Book])
async def retrieve_a_list_of_books(author_id=None, skip: int = 0, limit: int = 20, manager=Depends(get_book_manager)):
    return manager.get_all_items(author_id, skip, limit)
