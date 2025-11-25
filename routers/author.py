from schemas import schemas_author

from sqlalchemy.orm import Session

from crud import crud_author

from fastapi import Depends, HTTPException, APIRouter

from session_db import db_session

router = APIRouter()


@router.get("/author/{author_id}", response_model=schemas_author.GetAuthor)
def get_author_id(author_id: int, db: Session = Depends(db_session)):
    return crud_author.get_author(db, author_id)


@router.get("/author/", response_model=list[schemas_author.GetAuthor])
def get_author_all(skip: int = 0, limit: int = 10, db: Session = Depends(db_session)):
    return crud_author.get_author(db, skip=skip, limit=limit)

@router.post("/author/", response_model=schemas_author.GetAuthor)
def create_author(author_create: schemas_author.CreateAuthor, db: Session = Depends(db_session)):
    db_author_name = crud_author.author_name(db, author_create.name)
    if db_author_name:
        raise HTTPException(
            status_code=400,
            detail= "Author exists"
        )
    return crud_author.create_author(db=db, create_authors=author_create)