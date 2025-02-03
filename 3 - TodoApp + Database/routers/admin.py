from typing import Annotated
from fastapi import APIRouter, Path, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status
from models import User
from database import session_local
from routers.auth import get_current_user , CreateUserRequest
from models import Todos



# Dependency to get database session
def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


# Define the router
router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


# Utility function to check for admin privileges
def ensure_admin(_user: dict):
    if _user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="You do not have permission to access this resource.")


# Get all users (admin only)
@router.get("/get-all-user", status_code=status.HTTP_200_OK)
async def get_users(_user: user_dependency, _db: db_dependency):
    ensure_admin(_user)  # Ensure the current user is an admin
    return _db.query(User).all()


# Get a specific user by username (admin only)
@router.get("/get-user/{username}", status_code=status.HTTP_200_OK)
async def get_user(username: str, _user: user_dependency, _db: db_dependency):
    ensure_admin(_user)  # Ensure the current user is an admin
    user = _db.query(User).filter(User.username == username).first()
    if user is not None:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")


# Update a user (admin only)
@router.put("/update-user/{username}", status_code=status.HTTP_200_OK)
async def update_user(
        username: str,
        user_request: CreateUserRequest,
        _user: user_dependency,
        _db: db_dependency
):
    ensure_admin(_user)  # Ensure the current user is an admin
    user = _db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Update the user's details
    user.username = user_request.username
    user.hashed_password = user_request.password  # Hash the password if needed
    user.email = user_request.email
    user.role = user_request.role
    user.is_active = user_request.is_active
    user.first_name = user_request.first_name
    user.last_name = user_request.last_name
    _db.commit()
    return {"message": f"User: {username} updated successfully"}


@router.delete("/delete-user/{username}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
        username: str,
        _user: user_dependency,
        _db: db_dependency):
    ensure_admin(_user)  # Ensure the current user is an admin
    user = _db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Delete all tweets associated with the user
    user_tweets = _db.query(Todos).filter(Todos.user_id == user.id).all()
    for tweet in user_tweets:
        _db.delete(tweet)

    # Delete the user
    _db.delete(user)
    _db.commit()

    return {"message": f"User: {username} and their tweets deleted successfully"}