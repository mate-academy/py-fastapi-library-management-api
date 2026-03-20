from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload, joinedload
from db.models import AuthorORM, BookORM
from schemas import AuthorAddDTO, BookAddDTO, AuthorPatchDTO


# =====================AUTHORS======================
def create_author(db: Session, new_author: AuthorAddDTO) -> AuthorORM:
    new_db_author = AuthorORM(
        name=new_author.name,
        bio=new_author.bio
    )
    db.add(new_db_author)
    db.commit()
    db.refresh(new_db_author)

    return new_db_author


def select_author_by_id(db: Session, author_id: int) -> AuthorORM | None:
    query = (
        select(AuthorORM)
        .where(AuthorORM.id == author_id)
        .options(selectinload(AuthorORM.books))
    )
    return db.execute(query).scalars().first()


def select_authors(db: Session, skip: int, limit: int) -> list[AuthorORM]:
    query = (
        select(AuthorORM)
        .offset(skip)
        .limit(limit)
        .options(selectinload(AuthorORM.books))
    )
    return db.execute(query).scalars().all() # type: ignore


def select_author_by_name(db: Session, name: str) -> AuthorORM | None:
    query = (
        select(AuthorORM)
        .where(AuthorORM.name == name)
    )
    return db.execute(query).scalars().first()


def remove_author(db: Session, delete_author: AuthorORM): 
    db.delete(delete_author)
    db.commit()
    return


def update_author(db: Session, db_author_to_patch: AuthorORM, author_model: AuthorPatchDTO):
    author_model_dict = author_model.model_dump()

    for key,value in author_model_dict.items():
        if value:
            setattr(db_author_to_patch, key, value)
    db.commit()
    db.refresh(db_author_to_patch)
    return db_author_to_patch
    

# =====================BOOKS======================
def create_book(db: Session, new_book: BookAddDTO) -> BookORM:
    new_book_db = BookORM(
        title=new_book.title,
        summary=new_book.summary,
        publication_date=new_book.publication_date,
        author_id=new_book.author_id
    )
    db.add(new_book_db)
    db.commit()
    db.refresh(new_book_db)

    return new_book_db


def select_books(db: Session, skip: int, limit: int) -> list[BookORM]:
    query = (
        select(BookORM)
        .offset(skip)
        .limit(limit)
        .options(joinedload(BookORM.author))
    )
    return db.execute(query).scalars().all() # type: ignore
