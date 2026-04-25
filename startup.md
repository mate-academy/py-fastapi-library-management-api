<!-- @format -->

# Run the application:

python main.py or

uvicorn main:app --reload

# Access the API documentation:

Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc

# API Endpoints Summary

## Authors

POST /authors/ - Create a new author

GET /authors/ - Get all authors with pagination (skip, limit)

GET /authors/{author_id} - Get author by ID (includes their books)

PUT /authors/{author_id} - Update an author

DELETE /authors/{author_id} - Delete an author

GET /authors/{author_id}/books/ - Get books for a specific author

## Books

POST /books/ - Create a new book

GET /books/ - Get all books with pagination and optional author_id filter

GET /books/{book_id} - Get book by ID

PUT /books/{book_id} - Update a book

DELETE /books/{book_id} - Delete a book

## Example API Requests

Create an author

curl -X POST "http://localhost:8000/authors/" \

-H "Content-Type: application/json" \

-d '{"name":"Jane Austen","bio":"English novelist known for Pride and Prejudice"}'

Create a book for an author

curl -X POST "http://localhost:8000/books/" \
 -H "Content-Type: application/json" \
 -d '{"title":"Pride and Prejudice","summary":"A classic romance novel","publication_date":"1813-01-28","author_id":1}'

Get books filtered by author

curl "http://localhost:8000/books/?author_id=1&skip=0&limit=10"
