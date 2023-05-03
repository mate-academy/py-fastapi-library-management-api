from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal
from deps import get_current_user
from utils import verify_password, create_access_token, create_refresh_token

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def get_author(db: Session, author_id: int) -> schemas.Author:
    author = crud.get_author_by_id(db=db, author_id=author_id)

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    return author


def get_book(db: Session, book_id: int) -> schemas.Book:
    book = crud.get_book_by_id(db=db, book_id=book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return book


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
    search_name: str = None,
    sorting_column: str = None,
    ascending: bool = True
):
    if sorting_column and sorting_column not in schemas.Author.__fields__:
        raise HTTPException(
            status_code=404,
            detail="Author doesn't have such field"
        )

    return crud.get_author_list(
        db=db,
        search_name=search_name,
        sorting_column=sorting_column,
        ascending=ascending
    )[skip:skip + limit]


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def get_one_author(author_id: int, db: Session = Depends(get_db)):
    author = get_author(db=db, author_id=author_id)

    return author


@app.post("/authors/", response_model=schemas.Author)
def create_author(
    author: schemas.AuthorCreate,
    user: schemas.UserAuth = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_author = crud.get_author_by_name(db=db, name=author.name)

    if db_author:
        raise HTTPException(
            status_code=400, detail="Such author already exists"
        )

    return crud.create_author(db=db, author=author)


@app.put("/authors/{author_id}/", response_model=schemas.Author)
def update_author(
    author: schemas.AuthorCreate,
    author_id: int,
    user: schemas.UserAuth = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    get_author(db=db, author_id=author_id)

    return crud.update_author(db=db, author=author, author_id=author_id)


@app.patch("/authors/{author_id}/", response_model=schemas.Author)
def partial_update_author(
    author: schemas.AuthorPartialUpdate,
    author_id: int,
    user: schemas.UserAuth = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    get_author(db=db, author_id=author_id)

    return crud.partial_update_author(
        db=db, author=author, author_id=author_id
    )


@app.delete("/authors/{author_id}/")
def delete_author(
    author_id: int,
    user: schemas.UserAuth = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    get_author(db=db, author_id=author_id)

    return crud.delete_author(db=db, author_id=author_id)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
    db: Session = Depends(get_db),
    author_id: int = None,
    skip: int = 0,
    limit: int = 10,
    book_title: str = None,
    sorting_column: str = None,
    ascending: bool = True
):
    if sorting_column and sorting_column not in schemas.Book.__fields__:
        raise HTTPException(
            status_code=404,
            detail="Book doesn't have such field"
        )

    return crud.get_book_list(
        db=db,
        author_id=author_id,
        book_title=book_title,
        sorting_column=sorting_column,
        ascending=ascending
    )[skip:skip + limit]


@app.post("/books/", response_model=schemas.Book)
def create_book(
    book: schemas.BookCreate,
    user: schemas.UserAuth = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    get_author(db=db, author_id=book.author_id)

    return crud.create_book(db=db, book=book)


@app.put("/books/{book_id}/", response_model=schemas.Book)
def update_book(
    book: schemas.BookCreate,
    book_id: int,
    user: schemas.UserAuth = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    get_author(db=db, author_id=book.author_id)

    get_book(db=db, book_id=book_id)

    return crud.update_book(db=db, book=book, book_id=book_id)


@app.patch("/books/{book_id}/", response_model=schemas.Book)
def partial_update_book(
    book: schemas.BookPartialUpdate,
    book_id: int,
    user: schemas.UserAuth = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if book.author_id:
        get_author(db=db, author_id=book.author_id)

    get_book(db=db, book_id=book_id)

    return crud.partial_update_book(db=db, book=book, book_id=book_id)


@app.delete("/books/{book_id}/")
def delete_book(
    book_id: int,
    user: schemas.UserAuth = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    get_book(db=db, book_id=book_id)

    return crud.delete_book(db=db, book_id=book_id)


@app.post(
    "/signup/", summary="Create new user", response_model=schemas.UserOut
)
def create_user(user: schemas.UserAuth, db: Session = Depends(get_db)):

    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(
            status_code=400, detail="Such user already exists"
        )

    return crud.create_user(db=db, user=user)


@app.post("/login/", response_model=schemas.TokenSchema)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = crud.get_user_by_email(db, form_data.username)
    if user is None:
        raise HTTPException(
            status_code=400,
            detail="Incorrect email or password"
        )

    hashed_pass = user.hashed_password
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=400,
            detail="Incorrect email or password"
        )

    return {
        "access_token": create_access_token(user.email),
        "refresh_token": create_refresh_token(user.email),
    }


@app.get("/me/", response_model=schemas.UserOut)
def get_me(user: schemas.UserAuth = Depends(get_current_user)):
    return user
