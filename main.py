from datetime import date
from typing import Annotated

from uvicorn import run
from fastapi import FastAPI, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from db.database import SessionCreator
import crud
from schemas import AuthorDTO, AuthorAddDTO, BookDTO, BookAddDTO, AuthorRelDTO, BookRelDTO, AuthorPatchDTO
from db.create_db import create_tables, insert_data


app = FastAPI()

def get_db():
    db = SessionCreator()
    try:
        yield db
    finally:
        db.close()

AuthorExistsError = HTTPException(status_code=400, detail="Author with same name data exists!")
AuthorNotFoundError =  HTTPException(status_code=404, detail="Author not found!")
DataBase = Annotated[Session, Depends(get_db)]

# =====================AUTHORS======================
@app.post("/author/", response_model=AuthorDTO)
def new_author(
    db: DataBase,
    new_author: AuthorAddDTO = AuthorAddDTO(
        name="Author Name",
        bio="Author bio"
    )
):
    check_if_author_exists = crud.select_author_by_name(db=db, name=new_author.name)
    if check_if_author_exists:
        raise AuthorExistsError
    return crud.create_author(
        db=db,
        new_author=new_author
    )


@app.get("/author/{author_id}", response_model=AuthorRelDTO)
def get_single_author(
    db: DataBase,
    author_id: int = 0,
):
    selected_author = crud.select_author_by_id(db=db, author_id=author_id)
    if not selected_author:
        raise AuthorNotFoundError
    return selected_author


@app.get("/author/", response_model=list[AuthorRelDTO])
def get_list_of_authors(
    db: DataBase,
    skip: int = 0,
    limit: int = 3,
):
    return crud.select_authors(db=db, skip=skip, limit=limit)


@app.delete("/author/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_author(
    author_id: int,
    db: DataBase
):
    author_to_delete = crud.select_author_by_id(db=db, author_id=author_id)
    if not author_to_delete:
        raise AuthorNotFoundError

    crud.remove_author(db=db, delete_author=author_to_delete)    

    return None


@app.patch("/author/", response_model=AuthorRelDTO)
def patch_author(
    author_model: AuthorPatchDTO,
    db: DataBase,
    author_name: str | None = None,
    author_id: int | None = None,
):
    def name_exist(name: str):
        return crud.select_author_by_name(db=db, name=name)

    if author_name and  not author_id:
        selected_author = name_exist(author_name)

    elif author_id and not author_name:
        selected_author = crud.select_author_by_id(db=db, author_id=author_id)
        
    elif author_name and author_id:
        selected_author_by_id = crud.select_author_by_id(db=db, author_id=author_id)
        selected_author_by_name = name_exist(author_name)
        if not selected_author_by_name or not selected_author_by_id:
            raise HTTPException(status_code=404, detail="Wrong data entered!")
        if selected_author_by_id.id != selected_author_by_name.id:
            raise HTTPException(status_code=400, detail="Author name and ID mismatch")
        selected_author = selected_author_by_id

    else:
        raise AuthorNotFoundError

    if not selected_author:
        raise AuthorNotFoundError

    if author_model.name:
        existing_with_new_name = name_exist(author_model.name)
        if existing_with_new_name and existing_with_new_name.id != selected_author.id:
            raise AuthorExistsError

    return crud.update_author(db=db, db_author_to_patch=selected_author, author_model=author_model)


# =====================BOOKS======================
@app.post("/book/", response_model=BookDTO)
def new_book(
    db: DataBase,
    new_book: BookAddDTO = BookAddDTO(
        title="Books title",
        summary="Books summary",
        publication_date=date.today(),
        author_id=0
        )
    ):
    book_author = crud.select_author_by_id(db=db, author_id=new_book.author_id)
    if not book_author:
        raise AuthorExistsError
    return crud.create_book(db=db, new_book=new_book)


@app.get("/book/{author_id}", response_model=list[BookDTO])
def get_books_by_author(
    author_id: int,
    db: DataBase
):
    author = crud.select_author_by_id(db=db, author_id=author_id)

    if not author:
        raise AuthorNotFoundError

    return author.books

@app.get("/book/", response_model=list[BookRelDTO])
def get_list_of_books(
    db: DataBase,
    skip: int = 0,
    limit: int = 3,
):
    return crud.select_books(db=db, skip=skip, limit=limit)


if __name__=="__main__":
    create_tables()
    insert_data()
    run("main:app", host="127.0.0.1", port=8000, reload=True)
