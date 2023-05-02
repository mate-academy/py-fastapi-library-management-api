from fastapi import HTTPException

from app import crud


def get_author_or_404(author_id, db):
    db_author = crud.get_author_by_id(author_id=author_id, db=db)
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


def get_book_or_404(book_id, db):
    db_book = crud.get_book_by_id(db=db, book_id=book_id)
    if not db_book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )
    return db_book
