from fastapi import FastAPI, Depends
from fastapi_pagination import add_pagination, Page, paginate
from sqlalchemy.orm import Session
from crud import get_many, get_one, update_item, get_books, add_book, add_item, delete_item
from database import get_session
from models import DBAuthor, DBBook
from schemas import AuthorWithId, AuthorNoId, BookWithId, BookNoId

app = FastAPI(title="Library Manager")


@app.get("/authors/", response_model=Page[AuthorWithId])
def read_authors(db_session: Session = Depends(get_session)):
    return paginate(get_many(db_session=db_session, db_model=DBAuthor))


@app.get("/authors/{ident:int}/", response_model=AuthorWithId)
def read_author(ident, db_session: Session = Depends(get_session)):
    return get_one(ident=ident, db_session=db_session, db_model=DBAuthor)


@app.post("/authors/", response_model=AuthorNoId)
def create_author(author_data: AuthorNoId, db_session: Session = Depends(get_session)):
    return add_item(db_session=db_session, item_data=author_data, db_model=DBAuthor)


@app.patch("/authors/{ident:int}/", response_model=AuthorNoId)
def update_author(ident, update_data: AuthorNoId, db_session: Session = Depends(get_session)):
    return update_item(ident=ident, update_data=update_data, db_session=db_session, db_model=DBAuthor)


@app.delete("/authors/{ident:int}/")
def delete_author(ident, db_session: Session = Depends(get_session)):
    return delete_item(ident=ident, db_session=db_session, db_model=DBAuthor)


@app.get("/books/", response_model=Page[BookWithId])
def read_books(db_session: Session = Depends(get_session), author_ids: str | None = None):
    return paginate(get_books(db_session=db_session, author_ids=author_ids))


@app.get("/books/{ident:int}/", response_model=BookWithId)
def read_book(ident, db_session: Session = Depends(get_session)):
    return get_one(ident=ident, db_session=db_session, db_model=DBBook)


@app.post("/books/", response_model=BookNoId)
def create_book(book_data: BookNoId, db_session: Session = Depends(get_session)):
    return add_book(db_session=db_session, book_data=book_data)


@app.patch("/books/{ident:int}/", response_model=BookNoId)
def update_book(ident, update_data: BookNoId, db_session: Session = Depends(get_session)):
    return update_item(ident=ident, update_data=update_data, db_session=db_session, db_model=DBBook)


@app.delete("/books/{ident:int}/")
def delete_book(ident, db_session: Session = Depends(get_session)):
    return delete_item(ident=ident, db_session=db_session, db_model=DBBook)


add_pagination(app)
