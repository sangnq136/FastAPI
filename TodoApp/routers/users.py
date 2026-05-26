from typing import Annotated
from fastapi import Depends, HTTPException, Path, APIRouter
from passlib.context import CryptContext
from pydantic import BaseModel, Field
from starlette import status
from ..database import SessionLocal
from ..models import Users
from .auth import get_current_user

router = APIRouter(
    prefix="/user",
    tags=["user"],
)
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# dependency inject
db_dependency = Annotated[SessionLocal, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class UserRequest(BaseModel):
    password: str
    new_password: str = Field(min_length=6)
@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
    return db.query(Users).all()

@router.get("/detail", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
    return db.query(Users).filter(Users.id == user.get('id')).first()
@router.put("/change_password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user:user_dependency, db: db_dependency, user_request: UserRequest):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if user_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")
    if not bcrypt_context.verify(user_request.password, user_model.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Old Password")
    user_model.hashed_password = bcrypt_context.hash(user_request.new_password)

    db.add(user_model)
    db.commit()

@router.put("/change_phone", status_code=status.HTTP_204_NO_CONTENT)
async def change_phone(user:user_dependency, db: db_dependency, phone_number : str ):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if user_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")
    user_model.phone_number = phone_number

    db.add(user_model)
    db.commit()