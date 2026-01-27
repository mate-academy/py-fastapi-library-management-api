from typing import List

from sqlmodel import select

from fastapi import APIRouter, Query, HTTPException, status

from database import SessionDep

from models import Author

from schemas import AuthorUpdate


router = APIRouter()

@router.post("/author/", response_model=Author)
def create_author(author: Author, session: SessionDep) -> Author:
    session.add(author)
    session.commit()
    session.refresh(author)
    return author


@router.get("/authors/", response_model=List[Author])
def read_author(
        session: SessionDep,
        limit: int = Query(1, ge=1, le=100),
        offset: int = Query(0, ge=0),
) -> List[Author]:

    statement = select(Author).offset(offset).limit(limit)

    return session.exec(statement).all()


@router.put("/author/{author_id}", response_model=Author)
def update_author(
        author_id: int,
        author_data: AuthorUpdate,
        session: SessionDep,
) -> Author:
    author = session.get(Author, author_id)

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    for key, value in author_data.model_dump(exclude_unset=True).items():
        setattr(author, key, value)

    session.commit()
    session.refresh(author)
    return author


@router.delete("/author/{author_id}", status_code=status.HTTP_204_NO_CONTENT,)
def delete_author(
        author_id: int,
        session: SessionDep,
) -> None:

    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    session.delete(author)
    session.commit()

