from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud
from database import SessionLocal
from schemas import AuthorList, AuthorCreate, BookList, BookCreate
from fastapi_pagination import Page, add_pagination, paginate

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=Page[AuthorList])
def get_authors(db: Session = Depends(get_db)) -> Page[AuthorList]:
    return paginate(crud.get_all_authors(db=db))


@app.get("/authors/{author_id}/", response_model=AuthorList)
def get_author_by_id(
        author_id: int,
        db: Session = Depends(get_db)
) -> AuthorList:
    db_author = crud.get_author_by_id(db=db, author_id=author_id)
    if db_author:
        return db_author
    raise HTTPException(
        status_code=404,
        detail="Author not found"
    )


@app.post("/authors/", response_model=AuthorList)
def create_author(
        author: AuthorCreate,
        db: Session = Depends(get_db),

) -> AuthorList:
    db_author = crud.get_author_by_name(name=author.name)
    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Authos with this name already exists"
        )
    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=Page[BookList])
def get_books(
        author_id: int | None = None,
        db: Session = Depends(get_db)
) -> Page[BookList]:
    return paginate(crud.get_all_books(db=db, author_id=author_id))


@app.post("/books/", response_model=BookList)
def create_book(
        book: BookCreate,
        db: Session = Depends(get_db),
) -> BookList:
    return crud.create_book(db=db, book=book)


add_pagination(app)
