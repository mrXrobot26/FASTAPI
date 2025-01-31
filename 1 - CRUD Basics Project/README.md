# FastAPI Books API

This is a simple FastAPI-based RESTful API for managing books. The API supports CRUD operations, searching books by author and category, and organizing books into categories.

## Features
- Retrieve all books
- Retrieve a book by ID
- Retrieve books by category
- Search books by category
- Retrieve books by author within a category
- Create, update, and delete books

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

### Get Books by Category
```http
GET /books-by-category
```
Returns books grouped by their categories.

### Search Books by Category
```http
GET /search_books_by_categoryt/{category}
```
Returns books that match the given category.

### Get Books by Author Within a Category
```http
GET /books-for-auth-within-category/{author}?category={category}
```
Returns books written by a specific author within an optional category.

### Create a New Book
```http
POST /books
```
Creates a new book. Example request body:
```json
{
    "id": 12,
    "title": "New Book Title",
    "book": "Book12",
    "author": "Author 12",
    "category": "New Category"
}
```

### Update a Book
```http
PUT /books/{book_id}
```
Updates an existing book by ID. Example request body:
```json
{
    "title": "Updated Title"
}
```

### Delete a Book
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
