from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

import crud
import schemas
from database import get_db, Base, engine

# Створення таблиць у базі даних при старті додатку
Base.metadata.create_all(bind=engine)

# Створення FastAPI додатку
app = FastAPI(title="Library Management API", version="1.0.0")


# ========== ENDPOINTS ДЛЯ АВТОРІВ ==========

@app.post("/authors/", response_model=schemas.Author, status_code=201)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    """
    Створення нового автора.
    """
    try:
        db_author = crud.create_author(db=db, author=author)
        return db_author
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, 
            detail=f"Author with name '{author.name}' already exists"
        )


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
    skip: int = Query(0, ge=0, description="Кількість записів для пропуску"),
    limit: int = Query(10, ge=1, le=100, description="Максимальна кількість записів"),
    db: Session = Depends(get_db)
):
    """
    Отримання списку авторів з пагінацією.
    - **skip**: кількість записів для пропуску (для пагінації)
    - **limit**: максимальна кількість записів для повернення (максимум 100)
    """
    authors = crud.get_authors(db, skip=skip, limit=limit)
    return authors


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    """
    Отримання автора за ID.
    """
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


# ========== ENDPOINTS ДЛЯ КНИГ ==========

@app.post("/books/", response_model=schemas.Book, status_code=201)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    """
    Створення нової книги для конкретного автора.
    """
    # Перевірка, чи існує автор
    db_author = crud.get_author(db, author_id=book.author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    
    db_book = crud.create_book(db=db, book=book)
    return db_book


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
    skip: int = Query(0, ge=0, description="Кількість записів для пропуску"),
    limit: int = Query(10, ge=1, le=100, description="Максимальна кількість записів"),
    author_id: int | None = Query(None, description="Фільтр за ID автора"),
    db: Session = Depends(get_db)
):
    """
    Отримання списку книг з пагінацією та фільтрацією за автором.
    - **skip**: кількість записів для пропуску (для пагінації)
    - **limit**: максимальна кількість записів для повернення (максимум 100)
    - **author_id**: опціональний фільтр за ID автора
    """
    books = crud.get_books(db, skip=skip, limit=limit, author_id=author_id)
    return books


@app.get("/books/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    """
    Отримання книги за ID.
    """
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
