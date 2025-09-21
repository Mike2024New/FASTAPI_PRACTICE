from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from UTILS.HASH_MANAGER import HashManager
from ..BASE.schemas import UserCreate, UserBase
from ..BASE.database import get_db
from ..BASE.crud import CrudManager

router = APIRouter(prefix="/users", tags=["users"])
hash_manager = HashManager(secret_key="secret")  # такой примитивный секретный ключ просто для примера


@router.get("/", response_model=list[UserBase], status_code=status.HTTP_200_OK,
            summary="Получение всех пользователей")
def get_users_all_api(db: Annotated[Session, Depends(get_db)]):
    return CrudManager.get_users_all(db=db)


@router.get("/{username}/", response_model=UserBase, status_code=status.HTTP_200_OK,
            summary="Получение пользователя по конкретному id")
def get_user_by_username_api(username: str, db: Annotated[Session, Depends(get_db)]):
    user = CrudManager.get_user_by_username(db=db, username=username)
    if not user:
        raise HTTPException(status_code=404, detail=f"Пользователя с логином '{username}' не существует")
    return user


@router.post("/", response_model=UserBase, status_code=status.HTTP_201_CREATED,
             summary="Создание нового пользователя")
def add_new_user(user: UserCreate, db: Annotated[Session, Depends(get_db)]):
    # проверки при регистрации
    if CrudManager.get_user_by_username(username=user.username, db=db):
        raise HTTPException(status_code=400, detail=f"Пользователь с логином '{user.username}' уже существует.")
    hash_password = hash_manager.hash_password(password_in=user.password)
    user = CrudManager.add_new_user(db, username=user.username, password=hash_password)
    return user


@router.delete("/", response_model=UserBase, status_code=status.HTTP_200_OK,
               summary="Удаление пользователя по логину->username, метод будет защищён от случайного удаления через сессию и токен")
def del_user_by_username(username: str, db: Annotated[Session, Depends(get_db)]):
    user = CrudManager.del_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail=f"Пользователя с логином '{username}' не существует")
    return user
