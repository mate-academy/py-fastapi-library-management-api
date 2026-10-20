# Library Management API

## Task

Create a Simple Library Management API

### Objective
You should develop a basic library management API using FastAPI and SQLAlchemy ORM with SQLite as the database.

### Requirements

1. Set up the project structure with the following files:
```
- main.py
- database.py
- models.py
- schemas.py
- crud.py
```
2. Set up a SQLite database connection in the `database.py` file.

3. Create SQLAlchemy models for 'Author' and 'Book' in the `models.py` file.

4. The 'Author' model should have the following fields:
```
- id (integer, primary key)
- name (string, unique)
- bio (string)
- books (relationship with the 'Book' model, one-to-many)
```
5. The 'Book' model should have the following fields:
```
- id (integer, primary key)
- title (string)
- summary (string)
- publication_date (date)
- author_id (foreign key referencing 'Author' model)
```
6. Create Pydantic models for data validation and serialization in the `schemas.py` file.

7. Create CRUD utility functions for authors and books in the `crud.py` file.

8. In the `main.py` file, integrate the parts created in previous steps to build the FastAPI application:
   - Create the database tables using the SQLAlchemy models.
   - Define the FastAPI application object.
   - Create a dependency function to manage database sessions.
   - Implement API endpoints for the following actions:
     - Create a new author.
     - Retrieve a list of authors with pagination (skip, limit).
     - Retrieve a single author by ID.
     - Create a new book for a specific author.
     - Retrieve a list of books with pagination (skip, limit).
     - Filter books by author ID.
     
Upon completion, you should have a functional library management API that allows the user to manage authors and their books.

## Run the API

Create a virtual environment, install the dependencies, and start the development
server:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

The interactive API documentation is available at
`http://127.0.0.1:8000/docs`.

### Endpoints

- `POST /authors/` — create an author.
- `GET /authors/?skip=0&limit=100` — list authors.
- `GET /authors/{author_id}` — retrieve one author and their books.
- `POST /authors/{author_id}/books/` — create a book for an author.
- `GET /books/?skip=0&limit=100` — list books.
- `GET /books/?author_id={author_id}` — filter books by author.
