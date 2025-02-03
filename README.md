

# FastAPI Multi-Project Repository

This repository contains three separate FastAPI projects:

1. **FastAPI Todo & User Management Application**  
   A complete application for managing users (with admin and regular roles) and their todos, including JWT authentication and role-based access control.

2. **FastAPI Books API (Version 1)**  
   A RESTful API for managing books with support for CRUD operations, searching by category, grouping by category, and filtering books by author within a category.

3. **FastAPI Books API (Version 2)**  
   A RESTful API for managing books that features CRUD operations, searching by rating (1-5) and published year (1991-2025), along with data validation and exception handling.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Projects](#projects)
  - [1. FastAPI Todo & User Management Application](#1-fastapi-todo--user-management-application)
  - [2. FastAPI Books API (Version 1)](#2-fastapi-books-api-version-1)
  - [3. FastAPI Books API (Version 2)](#3-fastapi-books-api-version-2)
- [Installation & Setup](#installation--setup)
- [Running the Projects](#running-the-projects)
- [Contribution](#contribution)
- [License](#license)

---

## Project Overview

This repository demonstrates various FastAPI applications that show different aspects of building RESTful APIs using FastAPI and SQLAlchemy. The projects include:

- **User and Todo Management:**  
  User authentication with JWT tokens, role-based access (admin vs. regular users), and CRUD operations on todos.

- **Books APIs:**  
  Two variants of a Books API:
  - **Version 1** focuses on managing books with category grouping and filtering by author within a category.
  - **Version 2** adds extra endpoints to search books by rating and published year, with built-in data validation and robust exception handling.

Each project is self-contained, yet they share many common concepts such as database interaction, data validation using Pydantic, and interactive API documentation via Swagger UI/ ReDoc.

---

## Projects

### 1. FastAPI Todo & User Management Application

**Features:**

- **User Authentication:**  
  JWT-based login; token payload includes username, user ID, and role.
  
- **Role-Based Access:**  
  - **Admin Endpoints:** Manage users (list, update, delete).
  - **Regular Users:** Can manage their own todos.
  
- **Todo CRUD Operations:**  
  Create, update, read, and delete todos linked to authenticated users.

**API Endpoints Include:**

- **Authentication & Users (under `/auth` and `/admin`):**  
  - `POST /auth/token` – Login and receive JWT token.
  - `POST /auth/create-user` – Register a new user.
  - Admin endpoints for listing all users, retrieving a user by username, updating, and deleting users.
  
- **Todos (under `/todos`):**  
  - `GET /todos` – Retrieve all todos for the authenticated user.
  - `GET /todos/{item_id}` – Retrieve a specific todo.
  - `POST /todos` – Create a new todo.
  - `PUT /todos/{todo_item_id}` – Update an existing todo.
  - `DELETE /todos/{todo_item_id}` – Delete a todo.

---

### 2. FastAPI Books API (Version 1)

**Features:**

- CRUD operations for managing books.
- Retrieve all books.
- Retrieve a book by its ID.
- Retrieve books grouped by category.
- Search books by category.
- Retrieve books by a specific author within a given category.

**API Endpoints Include:**

- **Books Retrieval:**  
  - `GET /books` – List all books.
  - `GET /books/{book_id}` – Get details of a specific book.
  - `GET /books-by-category` – List books grouped by their categories.
  - `GET /search_books_by_categoryt/{category}` – Search for books by category.
  - `GET /books-for-auth-within-category/{author}?category={category}` – Retrieve books by an author within an optional category.

- **Books Management:**  
  - `POST /books` – Create a new book.
  - `PUT /books/{book_id}` – Update an existing book.
  - `DELETE /books/{book_id}` – Delete a book.

---

### 3. FastAPI Books API (Version 2)

**Features:**

- CRUD operations for managing books.
- Retrieve all books.
- Retrieve a book by its ID.
- Retrieve books filtered by rating (1-5).
- Retrieve books filtered by published year (1991-2025).
- Data validation and exception handling with proper status codes.
- Interactive API documentation through Swagger UI and ReDoc.

**API Endpoints Include:**

- **Books Retrieval:**  
  - `GET /books` – List all books.
  - `GET /books/{book_id}` – Get details of a specific book.
  - `GET /books/rating/{rating}` – Retrieve books matching a specific rating.
  - `GET /books/year/{year}` – Retrieve books published in a specific year.
  
- **Books Management:**  
  - `POST /books/create-book` – Create a new book.
  - `PUT /books/{book_id}` – Update an existing book.
  - `DELETE /books/{book_id}` – Delete a book.

---

## Installation & Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/mrXrobot26/FASTAPI.git
   cd FASTAPI
   ```

2. **Create and Activate a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   The common dependencies include:
   - FastAPI
   - Uvicorn
   - SQLAlchemy
   - Pydantic
   - Python-JOSE (for JWT)
   - Passlib (with bcrypt)

> **Note:**  
> Each project uses SQLite for its database. The database file(s) will be created automatically on first run.

---

## Running the Projects

Each project can be run independently. Make sure to navigate to the corresponding project folder if they are organized into subdirectories, or adjust the command as necessary if they share a common main file.

### FastAPI Todo & User Management Application

```bash
uvicorn app:app --reload --host 127.0.0.1 --port 9005
```

Access the documentation at:  
- Swagger UI: [http://127.0.0.1:9005/docs](http://127.0.0.1:9005/docs)  
- ReDoc: [http://127.0.0.1:9005/redoc](http://127.0.0.1:9005/redoc)

### FastAPI Books API (Version 1)

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Access the documentation at:  
- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### FastAPI Books API (Version 2)

If this version shares the same entry point (`main:app`) and port as Version 1, you might need to run it on a different port (or in a different virtual environment) to avoid conflicts:

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8001
```

Access the documentation at:  
- Swagger UI: [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs)  
- ReDoc: [http://127.0.0.1:8001/redoc](http://127.0.0.1:8001/redoc)

---

## Contribution

Contributions are welcome! Feel free to open issues or submit pull requests for improvements, bug fixes, or new features.

---

## License

This repository is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

