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

9. Optional tasks:
Search functionality:
Implement a search feature that allows users to search for authors or books by partial or complete names/titles. This can be added as a query parameter in the existing API endpoints for retrieving authors and books.

Sorting:
Add sorting functionality to the API endpoints for listing authors and books. Users should be able to sort the results based on various fields, such as name, title, or publication date, in ascending or descending order.

Update and delete operations:
Implement API endpoints for updating and deleting authors and books. This would provide a more complete CRUD (Create, Read, Update, and Delete) functionality for both authors and books.

Authentication and authorization:
Add authentication and authorization features to protect the API endpoints. This can be done using an authentication library like OAuth2 or JWT. Only authenticated users should be able to perform certain actions like creating, updating, or deleting authors and books.
