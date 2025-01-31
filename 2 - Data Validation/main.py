from typing import Optional
from fastapi import FastAPI, HTTPException ,Path
from fastapi.responses import RedirectResponse
from pydantic import BaseModel , Field

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    rating: int
    category: str
    published_year: int

    def __init__(self, id, title, author, rating, category, published_year):
        self.id = id
        self.title = title
        self.author = author
        self.rating = rating
        self.category = category
        self.published_year = published_year


class Book_Request(BaseModel):
    id: Optional[int] = Field(description='ID is not needed on create', default=None)
    title: str = Field(min_length=3, max_length=50)
    author: str = Field(min_length=3, max_length=50)
    rating: int = Field(gt=0, lt=6)
    category: str
    published_year: int = Field(gt=1990, lt=2026, description="Year must be a 4-digit number")

    model_config = {
        'json_schema_extra': {
            'example': {
                'title': 'The Great Gatsby',
                'author': 'F. Scott Fitzgerald',
                'rating': 5,
                'category': 'Classic',
                'published_year': 1999
            }
        }
    }


Books = [
    Book(1, "Book One", "Author One", 5, "Genre One", 2000),
    Book(2, "Book Two", "Author Two", 4, "Genre Two", 2000),
    Book(3, "Book Three", "Author Three", 5, "Genre Three", 2010),
    Book(4, "Book Four", "Author Four", 3, "Genre Four", 2010),
    Book(5, "Book Five", "Author Five", 4, "Genre Five", 2020),
    Book(6, "Book Six", "Author Six", 5, "Genre Six", 2020),
    Book(7, "Book Seven", "Author Seven", 4, "Genre Seven", 2025),
    Book(8, "Book Eight", "Author Eight", 3, "Genre Eight", 2025)
]

@app.get("/books")
async def get_all_posts():
    return Books


@app.get("/books/{book_id}")
async def get_book_by_id(book_id: int = Path(gt=0)):
    for book in Books:
        if book.id == book_id:
            return book
    return HTTPException(status_code=404, detail="Book not found")



@app.get("/books/rating/{rating}")
async def get_books_by_rating(rating: int = Path(gt=0, lt=6)):
    books_with_rating = [book for book in Books if book.rating == rating]
    if not books_with_rating:
        raise HTTPException(status_code=404, detail="No books found with the specified rating")
    return books_with_rating


@app.post("/books/create-book")
async def create_book(book_request: Book_Request):
    try:
        new_book = Book(**book_request.model_dump())
        new_book.id = Books[-1].id + 1 if Books else 1
        Books.append(new_book)
        return new_book
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



@app.put("/books/{book_id}")
async def update_book_by_id(book_request: Book_Request, book_id: int = Path(gt=0)):
    for book in Books:
        if book.id == book_id:
            book.title = book_request.title
            book.author = book_request.author
            book.rating = book_request.rating
            book.category = book_request.category
            book.published_year = book_request.published_year
            return book
    raise HTTPException(status_code=404, detail="Book not found")



@app.delete("/books/{book_id}")
async def delete_book_by_id(book_id: int = Path(gt=0) ):
    for book in Books:
        if book.id == book_id:
            Books.remove(book)
            return {"message": f"Book with ID {book_id} has been deleted"}
    raise HTTPException(status_code=404, detail="Book not found")



@app.get("/books/year/{year}")
async def get_books_by_year(year: int = Path(gt=1990, lt=2026)):
    books_with_year = [book for book in Books if book.published_year == year]
    if not books_with_year:
        raise HTTPException(status_code=404, detail="No books found for the specified year")
    return books_with_year




@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")