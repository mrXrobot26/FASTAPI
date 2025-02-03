# FastAPI Todo & User Management Application

This project is a FastAPI-based REST API that allows you to manage users and their todos. It implements user authentication, authorization (with admin and regular user roles), and CRUD operations for both users and todos.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Authentication & Roles](#authentication--roles)
- [Data Validation](#data-validation)
- [Installation & Setup](#installation--setup)
- [API Endpoints](#api-endpoints)
  - [Auth Endpoints](#auth-endpoints)
  - [User Endpoints (Admin Only)](#user-endpoints-admin-only)
  - [Todo Endpoints](#todo-endpoints)
- [Database](#database)
- [Running the Application](#running-the-application)
- [Notes](#notes)

## Features

- **User Authentication**: Secure endpoints using JWT Bearer tokens.
- **Role-Based Access Control**: Admin users have exclusive access to specific routes (user management endpoints).
- **User Registration**: Create a new user with validated input data.
- **CRUD Operations for Todos**: Create, read, update, and delete todos for authenticated users.
- **Data Validation**: All endpoints validate incoming data using [Pydantic](https://pydantic-docs.helpmanual.io/).

## Project Structure

```
├── app.py                  # Main FastAPI app file, includes routers and DB setup
├── database.py             # Database connection, SQLAlchemy engine and session creation
├── models.py               # SQLAlchemy models (User, Todos)
├── routers
│   ├── auth.py             # Authentication endpoints (login, create user, token generation)
│   ├── admin.py            # Admin-only endpoints for managing users
│   └── todos.py            # Endpoints to manage todos for authenticated users
├── README.md               # This file
```

## Authentication & Roles

- **JWT-based Authentication**:  
  Users log in by submitting their username and password. If valid, the API returns a JWT token which must be provided in subsequent requests via the `Authorization` header with the `Bearer` scheme.

- **Roles**:
  - **admin**:  
    Admin users can access additional endpoints such as viewing all users, updating a user, or deleting a user along with their todos.
  - **regular user**:  
    Regular users can only manage their own todos. They cannot access admin-only endpoints.

- **Token Payload**:  
  The JWT token includes the username, user id, role, and an expiration timestamp.

## Data Validation

Data is validated using Pydantic models. For example:

- **User Data (`CreateUserRequest`)**:
  - `username`: Must be between 3 and 20 characters.
  - `password`: Must have a minimum length of 8 characters.
  - `email`: Must be a valid email address (length between 5 and 50 characters).
  - `first_name` and `last_name`: Must be between 3 and 20 characters.
  - `role`: Defines the user role (e.g., `admin` or other values).
  - `is_active`: Boolean flag indicating whether the user is active.

- **Todo Data (`TodoRequest`)**:
  - `title`: Must be between 3 and 50 characters.
  - `description`: Must be between 3 and 100 characters.
  - `completed`: Boolean flag indicating whether the todo is completed.
  - `priority`: An integer value between 1 and 5 (validated using a range constraint).

Example JSON for creating a Todo:

```json
{
  "title": "Buy groceries",
  "description": "Milk, Cheese, Pizza, Fruit, Tylenol",
  "completed": false,
  "priority": 1
}
```

## Installation & Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/fastapi-todo-user-management.git
   cd fastapi-todo-user-management
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate      # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   Make sure the following libraries (and their dependencies) are installed:
   - fastapi
   - uvicorn
   - sqlalchemy
   - pydantic
   - python-jose[cryptography]
   - passlib[bcrypt]

4. **Database Setup**

   This project uses SQLite. The database file (`todosApp.db`) will be automatically created in the project directory once the app is run, as the tables are created using SQLAlchemy’s `create_all`.

## API Endpoints

### Auth Endpoints

- **Obtain Token**  
  `POST /auth/token`  
  **Description**: Login using username and password to receive an access token.  
  **Request Form Data**:
  - `username`
  - `password`

- **Create User**  
  `POST /auth/create-user`  
  **Description**: Create a new user.  
  **Request Body (JSON)**:
  ```json
  {
    "username": "johndoe",
    "password": "yourpassword",
    "email": "john@example.com",
    "role": "admin",  // or other role value
    "is_active": true,
    "first_name": "John",
    "last_name": "Doe"
  }
  ```

### User Endpoints (Admin Only)

> **Note**: These endpoints require the authenticated user to have an `admin` role.

- **Get All Users**  
  `GET /admin/get-all-user`  
  **Description**: Retrieve a list of all users.

- **Get Specific User by Username**  
  `GET /admin/get-user/{username}`  
  **Description**: Retrieve details of a specific user.

- **Update User**  
  `PUT /admin/update-user/{username}`  
  **Description**: Update a user's information.  
  **Request Body**: Same structure as in user creation.

- **Delete User**  
  `DELETE /admin/delete-user/{username}`  
  **Description**: Delete a user and all of their associated todos.

### Todo Endpoints

> **Note**: These endpoints are for authenticated users managing their own todos.

- **Get All Todos**  
  `GET /todos`  
  **Description**: Retrieve all todos for the authenticated user.

- **Get Todo by ID**  
  `GET /todos/{item_id}`  
  **Description**: Retrieve a specific todo by its ID.

- **Create Todo**  
  `POST /todos`  
  **Description**: Create a new todo.  
  **Request Body (JSON)**:  
  ```json
  {
    "title": "Buy groceries",
    "description": "Milk, Cheese, Pizza, Fruit, Tylenol",
    "completed": false,
    "priority": 1
  }
  ```

- **Update Todo**  
  `PUT /todos/{todo_item_id}`  
  **Description**: Update an existing todo.
  
- **Delete Todo**  
  `DELETE /todos/{todo_item_id}`  
  **Description**: Delete a todo.

## Database

The application uses SQLite as its database. The SQLAlchemy models are defined in the `models.py` file:

- **User Model**:  
  Fields include `id`, `username`, `email`, `hashed_password`, `is_active`, `first_name`, `last_name`, and `role`.

- **Todos Model**:  
  Fields include `id`, `title`, `description`, `priority`, `completed`, and a foreign key `user_id` linking to the `User` model.

## Running the Application

You can run the application using Uvicorn:

```bash
uvicorn app:app --reload --host 127.0.0.1 --port 9005
```

- Open your browser and navigate to [http://127.0.0.1:9005/docs](http://127.0.0.1:9005/docs) to see the interactive API documentation generated by FastAPI.

## Notes

- **Password Security**:  
  Passwords are hashed using `passlib` with the bcrypt algorithm.
  
- **Error Handling**:  
  The API uses HTTP status codes (such as `404 Not Found`, `401 Unauthorized`, and `403 Forbidden`) to indicate errors. Transactions are rolled back on errors when creating todos.

- **Admin Privileges**:  
  Certain endpoints (under `/admin`) check for admin privileges by validating the `role` field from the JWT payload. Unauthorized attempts will result in a `403 Forbidden` response.

- **Validation**:  
  Pydantic models enforce constraints on inputs such as string length, integer range, and required fields, ensuring that only valid data is processed.
