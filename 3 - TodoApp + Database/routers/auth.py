from datetime import timedelta, datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import BaseModel, Field
from typing import Annotated
from sqlalchemy.orm import Session
from database import session_local
from models import User
from passlib.context import CryptContext


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)
#dependencies
db_dependency = Annotated[Session, Depends(get_db)]
form_dependency =Annotated[OAuth2PasswordRequestForm , Depends()]
# oauth2_bearer_dependency = Annotated[str, Depends(oauth2_bearer)] => ERROR

# passlib => CryptContext bcrypt lib
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#SECRETS =>  pip install "python-jose[cryptography]"
SECRET_KEY = 'f3a7c9e8b2d5f04a6c1e9b8d7f52a3e6c4d8b9a5f7e0c2d1a6b3f9e4d7c2a5b1'
ALGORITHM = 'HS256'

#Bearer
#  ما هو OAuth2PasswordBearer؟
# هو Dependency في FastAPI يُستخدم لاستخراج الـ access token من طلبات HTTP Bearer Token Authentication.
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

class CreateUserRequest(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=8)
    email: str  = Field(min_length=5, max_length=50)
    role: str
    is_active: bool = True
    first_name: str = Field(min_length=3, max_length=20)
    last_name: str = Field(min_length=3, max_length=20)

class Token(BaseModel):
    access_token: str
    token_type: str





def create_access_token(username: str, user_id: int, user_role :str , expires_delta: timedelta):
    payload = {"username": username,"user_id": user_id,"exp": datetime.now(timezone.utc) + expires_delta , "role": user_role}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username : str = payload.get("username")
        user_id : int = payload.get("user_id")
        role : str = payload.get("role")
        if username is None or user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"username": username, "user_id": user_id , "role": role}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def authenticate_user(username:str , password:str , db):
    user = db.query(User).filter(User.username == username).first()
    if user is not None and bcrypt_context.verify(password, user.hashed_password):
        return user
    else:
        return None

@router.post("/token")
async def login_for_access_token(form_data: form_dependency, _db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, _db)
    if user:
        token = create_access_token(user.username, user.id, user.role ,timedelta(minutes=30))
        return Token(access_token=token, token_type="bearer")
    else:
        raise HTTPException(status_code=404, detail="Incorrect username or password")


@router.post("/create-user")
async def get_users(user_request : CreateUserRequest , _db: db_dependency):
    user = _db.query(User).filter(User.username == user_request.username).first()
    if user is None:
        new_user = User(
            username=user_request.username,
            hashed_password=bcrypt_context.hash(user_request.password),
            email=user_request.email,
            role=user_request.role,
            is_active=user_request.is_active,
            first_name=user_request.first_name,
            last_name=user_request.last_name
        )
        _db.add(new_user)
        _db.commit()
        _db.refresh(new_user)
        return new_user
    else:
        return {"message": "User with this username already exists"}













# def create_access_token(username:str , user_id : int , expires_delta: timedelta):
#     encode = {"username": username,"user_id": user_id}
#     expires = datetime.now(timezone.utc) + expires_delta
#     encode.update({"exp": expires})
#     return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)




import uvicorn as uv

if __name__ == "__main__":
    uv.run(router, host="127.0.0.1", port=9005)
