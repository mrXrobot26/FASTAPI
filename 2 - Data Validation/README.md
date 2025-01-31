# FastAPI Books API

This is a FastAPI-based RESTful API for managing books. The API supports CRUD operations, searching books by rating and year, and provides validation, exception handling, and status codes.

## Features
- Retrieve all books
- Retrieve a book by ID
- Retrieve books by rating
- Retrieve books by published year
- Create, update, and delete books
- Data validation and exception handling
- Swagger UI documentation

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/mrXrobot26/FASTAPI.git
   cd FASTAPI
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

## API Endpoints

### Get All Books
```http
GET /books
```
Returns a list of all available books.

### Get Book by ID
```http
GET /books/{book_id}
```
Returns a specific book based on its ID.

### Get Books by Rating
```http
GET /books/rating/{rating}
```
Returns books that match the given rating (1-5).

### Get Books by Published Year
```http
GET /books/year/{year}
```
Returns books that match the specified year (1991-2025).

### Create a New Book
```http
POST /books/create-book
```
Creates a new book. Example request body:
```json
{
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "rating": 5,
    "category": "Classic",
    "published_year": 1999
}
```

### Update a Book by ID
```http
PUT /books/{book_id}
```
Updates an existing book by ID. Example request body:
```json
{
    "title": "Updated Title",
    "author": "Updated Author",
    "rating": 4,
    "category": "Updated Category",
    "published_year": 2015
}
```

### Delete a Book by ID
```http
DELETE /books/{book_id}
```
Deletes a book by ID.

## Running the API
After starting the server, you can access the interactive API documentation at:
- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Contribution
Feel free to contribute by creating issues or submitting pull requests.

## License
This project is licensed under the MIT License.

