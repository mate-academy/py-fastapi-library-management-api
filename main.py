from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    status,
    security
)
from sqlalchemy.orm import Session

import crud, schemas, utils


app = FastAPI()


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
    skip: int = 0,
    limit: int = 10,
    author_name: str | None = None,
    sort_field: str | None = None,
    db: Session = Depends(utils.get_db)
):
    return crud.get_author_list(
        db, skip=skip,
        limit=limit,
        author_name=author_name,
        sort_field=sort_field,
    )


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(utils.get_db)):
    author = crud.get_author(db, author_id=author_id)
    if author is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Author was not found"
        )
    return author


@app.post("/authors/", response_model=schemas.Author)
def create_author(
    author: schemas.AuthorCreate,
    db: Session = Depends(utils.get_db)
):
    db_author = crud.get_author_by_name(db, authorname=author.name)
    if db_author:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Author with such name already exists"
        )
    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
    skip: int = 0,
    limit: int = 10,
    author_id: int | None = None,
    book_title: str | None = None,
    sort_field: str | None = None,
    db: Session = Depends(utils.get_db)
):
    return crud.get_book_list(
        db=db,
        skip=skip,
        limit=limit,
        author_id=author_id,
        book_title=book_title,
        sort_field=sort_field,
    )


@app.get("/books/{book_id}/", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(utils.get_db)):
    book = crud.get_book(db, book_id=book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book was not found"
        )
    return book


@app.post("/books/", response_model=schemas.Book)
def create_book(
    book: schemas.BookCreate,
    db: Session = Depends(utils.get_db)
):
    db_book = crud.get_book_by_title(db, title=book.title)
    if db_book:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book with such title already exests"
        )
    return crud.create_book(db=db, book=book)


@app.patch("/books/{book_id}/", response_model=schemas.Book)
def patch_book(
    book_id: int,
    book: schemas.BookCreate,
    db: Session = Depends(utils.get_db)
):
    return crud.patch_book(
        book_id=book_id,
        db=db,
        book=book
    )


@app.delete("/books/{book_id}/")
def delete_book(book_id: int, db: Session = Depends(utils.get_db)):
    return crud.delete_book(
        book_id=book_id,
        db=db,
    )


@app.patch("/authors/{author_id}/", response_model=schemas.Author)
def patch_author(
    author_id: int,
    author: schemas.AuthorCreate,
    db: Session = Depends(utils.get_db)
):
    return crud.patch_author(
        author_id=author_id,
        db=db,
        author=author
    )


@app.delete("/authors/{author_id}/")
def delete_author(author_id: int, db: Session = Depends(utils.get_db)):
    return crud.delete_author(
        author_id=author_id,
        db=db
    )


@app.post("/users/")
def create_user(user: schemas.UserCreate, db: Session = Depends(utils.get_db)):
    db_user = crud.get_user_by_email(email=user.email, db=db)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with that email already exists"
        )
    user = crud.create_user(user=user, db=db)
    return utils.create_token(user=user)


@app.post("/token/")
def generate_token(
    form_data: security.OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(utils.get_db)
):
    user = utils.authenticate_user(
        email=form_data.username,
        password=form_data.password,
        db=db
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    access_token = utils.create_access_token(user=user)
    refresh_token = utils.create_refresh_token(user=user)
    return {"access_token": access_token, "refresh_token": refresh_token}


@app.get("/users/me/", response_model=schemas.User)
def get_user(user: schemas.User = Depends(utils.get_current_user)):
    return user
