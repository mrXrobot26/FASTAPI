from typing import Annotated
from fastapi import APIRouter, Path, HTTPException
from fastapi.params import Depends
from pydantic import Field, BaseModel
from sqlalchemy.orm import Session
from starlette import status
from models import Todos
from database import session_local
from routers.auth import get_current_user


# Dependency to get database session
def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


router = APIRouter()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


# Pydantic model for Todo
class TodoRequest(BaseModel):
    title: str = Field(min_length=3, max_length=50)
    description: str = Field(min_length=3, max_length=100)
    completed: bool
    priority: int = Field(gt=0, lt=6)

    model_config = {
        'json_schema_extra': {
            'example': {
                'title': 'Buy groceries',
                'description': 'Milk, Cheese, Pizza, Fruit, Tylenol',
                'completed': False,
                'priority': 1
            }
        }
    }


# Get all todos for the authenticated user
@router.get('/todos', status_code=status.HTTP_200_OK)
async def get_all_todos(_user: user_dependency, _db: db_dependency):
    return _db.query(Todos).filter(Todos.user_id == _user.get('user_id')).all()


# Get a single todo by ID for the authenticated user
@router.get('/todos/{item_id}', status_code=status.HTTP_200_OK)
async def get_todo_by_id(_user: user_dependency, _db: db_dependency, item_id: int = Path(gt=0)):
    todo_item = _db.query(Todos).filter(Todos.id == item_id, Todos.user_id == _user.get('user_id')).first()
    if todo_item is not None:
        return todo_item
    else:
        raise HTTPException(status_code=404, detail="Todo not found")


# Create a new todo for the authenticated user
@router.post('/todos', status_code=status.HTTP_201_CREATED)
async def create_todo(_user: user_dependency, todo_item: TodoRequest, _db: db_dependency):
    try:
        new_todo = Todos(**todo_item.model_dump(), user_id=_user.get('user_id'))
        _db.add(new_todo)
        _db.commit()
        _db.refresh(new_todo)  # Fetch the newly created Todo
        return new_todo
    except Exception as e:
        _db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


# Update an existing todo for the authenticated user
@router.put('/todos/{todo_item_id}', status_code=status.HTTP_200_OK)
async def update_todo_item(
        _user: user_dependency,
        _db: db_dependency,
        updated_todo: TodoRequest,
        todo_item_id: int = Path(gt=0)
):
    todo_item = _db.query(Todos).filter(Todos.id == todo_item_id, Todos.user_id == _user.get('user_id')).first()
    if todo_item is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    # Update fields
    todo_item.title = updated_todo.title
    todo_item.description = updated_todo.description
    todo_item.completed = updated_todo.completed
    todo_item.priority = updated_todo.priority
    _db.commit()
    _db.refresh(todo_item)
    return todo_item


# Delete an existing todo for the authenticated user
@router.delete('/todos/{todo_item_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo_item(_user: user_dependency, _db: db_dependency, todo_item_id: int = Path(gt=0)):
    todo_item = _db.query(Todos).filter(Todos.id == todo_item_id, Todos.user_id == _user.get('user_id')).first()
    if todo_item is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    _db.delete(todo_item)
    _db.commit()


