from typing import Annotated
from fastapi import FastAPI ,Path , HTTPException
from fastapi.params import Depends
from pydantic import Field , BaseModel
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import RedirectResponse

import models
from models import Todos
from database import engine, session_local


# Initialize required database settings
def setup_database():
    models.Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

# Initialize FastAPI app and setup database
app = FastAPI()
setup_database()

db_dependency = Annotated[Session, Depends(get_db)]

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


@app.get('/todos', status_code=status.HTTP_200_OK)
async def get_all_todos(_db: db_dependency):
    return _db.query(Todos).all()

@app.get('/get-todo-by-id/{item_id}', status_code= status.HTTP_200_OK)
async def get_todo_by_id(_db : db_dependency, item_id : int = Path(gt=0)):
    todo_item = _db.query(Todos).filter(Todos.id == item_id).first()
    if todo_item is not None:
        return todo_item
    else:
        raise HTTPException(status_code=404, detail="Todo not found")

@app.post('/create-todo', status_code=status.HTTP_200_OK)
async def create_todo(todo_item: TodoRequest, _db: db_dependency):
    try:
        new_todo = Todos(**todo_item.model_dump())
        _db.add(new_todo)
        _db.commit()
        return todo_item
    except Exception as e:
        _db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@app.put('/update-todo/{todo_item_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_todo_item(_db: db_dependency, updated_todo: TodoRequest ,todo_item_id: int = Path(gt=0)):
    todo_item = _db.query(Todos).filter(Todos.id == todo_item_id).first()
    if todo_item is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo_item.title = updated_todo.title
    todo_item.description = updated_todo.description
    todo_item.completed = updated_todo.completed
    todo_item.priority = updated_todo.priority
    _db.commit()

@app.delete('/delete-todo/{todo_item_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo_item(_db: db_dependency, todo_item_id: int = Path(gt=0)):
    todo_item = _db.query(Todos).filter(Todos.id == todo_item_id).first()
    if todo_item is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    _db.delete(todo_item)
    _db.commit()


@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")