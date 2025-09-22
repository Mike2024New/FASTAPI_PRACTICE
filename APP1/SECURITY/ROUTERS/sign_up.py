from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request, Cookie
from ..security import hash_manager
from ..BASE.schemas import UserCreate, UserBase, UserLogin
from ..BASE.database import get_db
from ..BASE.crud import CrudManager


router = APIRouter(prefix="/create_account", tags=["register"])

@router.post("/", response_model=UserBase, status_code=status.HTTP_201_CREATED,
             summary="Создание нового пользователя")
def add_new_user(user: UserCreate, db: Annotated[Session, Depends(get_db)]):
    # проверки при регистрации
    if CrudManager.get_user_by_username(username=user.username, db=db):
        raise HTTPException(
            status_code=400, detail=f"Пользователь с логином '{user.username}' уже существует.")
    hash_password = hash_manager.hash_password(password_in=user.password)
    user = CrudManager.add_new_user(
        db, username=user.username, password=hash_password)
    # гарантированный способ убать чувствительные поля
    return UserBase.model_validate(user)
