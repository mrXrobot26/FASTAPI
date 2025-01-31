import string

from fastapi import FastAPI, HTTPException, Body
from starlette.responses import RedirectResponse

app = FastAPI()
Books = [
    {'id': 1, 'title': 'The Quantum Realm', 'book': 'Book1', 'author': 'Author 1', 'category': 'Science'},
    {'id': 2, 'title': 'The History Explorer', 'book': 'Book2', 'author': 'Author 2', 'category': 'History'},
    {'id': 3, 'title': 'Fictional World', 'book': 'Book3', 'author': 'Author 3', 'category': 'Fiction'},
    {'id': 4, 'title': 'Adventures in Coding', 'book': 'Book4', 'author': 'Author 4', 'category': 'Technology'},
    {'id': 5, 'title': 'The Art of Cooking', 'book': 'Book5', 'author': 'Author 5', 'category': 'Cooking'},
    {'id': 6, 'title': 'Fitness for Everyone', 'book': 'Book6', 'author': 'Author 6', 'category': 'Health'},
    {'id': 7, 'title': 'The Quantum Realm', 'book': 'Book1', 'author': 'Author 1', 'category': 'Science'},
    {'id': 8, 'title': 'The History Explorer', 'book': 'Book2', 'author': 'Author 2', 'category': 'History'},
    {'id': 9, 'title': 'Fictional World', 'book': 'Book3', 'author': 'Author 3', 'category': 'Fiction'},
    {'id': 10, 'title': 'Adventures in Coding', 'book': 'Book4', 'author': 'Author 4', 'category': 'Technology'},
    {'id': 11, 'title': 'The Art of Cooking', 'book': 'Book5', 'author': 'Author 5', 'category': 'Cooking'},
]


@app.get('/books')
async def get_all_books():
    return Books

@app.get('/books/{book_id}')
async def get_book_by_id(book_id: int):
    # Find the book by ID
    book = next((book for book in Books if book['id'] == book_id), None)
    # Return 404 if book not found
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.get('/books-by-category')
async def get_books_by_category():
    from collections import defaultdict
    grouped_books = defaultdict(list)
    for book in Books:
        grouped_books[book['category']].append(book)
    return grouped_books


@app.get('/search_books_by_categoryt/{category}')
async def search_books_by_categoryt(category: str):
    from collections import defaultdict
    grouped_books = defaultdict(list)
    for book in Books:
        category_of_book_in_loop = book['category'].lower()
        if category_of_book_in_loop== category.lower() :
            grouped_books[book['category']].append(book)
    return grouped_books


@app.get('/books-for-auth-within-category/{author}')
async def get_books_for_auth_within_category(author: str, category: str):
    grouped_books = []
    for book in Books:
        if book['author'].lower() == author.lower():
            if not category or book['category'].lower() == category.lower():
                grouped_books.append(book)
    return grouped_books if grouped_books else {"message": "No books found for this author/category"}


@app.post('/books')
async def create_book(new_book = Body()):
    return Books.append(new_book)


@app.put('/books/{book_id}')
async def update_book(id : int , new_book : dict):
    for book in Books:
        if book['id'] == id:
            book.update(new_book)
            return book
    return {"message": "Book not found"}

@app.delete('/books/{book_id}')
async def delete_book(book_id : int):
    for book in Books:
        if book['id'] == book_id:
            Books.remove(book)
            return book




# Redirect root (`/`) to Swagger UI directly
@app.get("/", include_in_schema=False)
async def redirect_to_swagger():
    return RedirectResponse(url="/docs")
