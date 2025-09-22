from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from ..security import hash_manager, jwt_manager
from ..BASE.schemas import UserBase
from ..BASE.database import get_db
from ..BASE.crud import CrudManager
from ..dependencies import get_user_from_token

router = APIRouter(tags=["login"])


@router.get("/test/", dependencies=[Depends(get_user_from_token)])
def test_func():
    print(123)
    return {"msg": "секретный контент"}


@router.post("/login/", status_code=status.HTTP_200_OK, response_model=UserBase)
def login_user_set_token_session(
    response: Response,
    db: Annotated[Session, Depends(get_db)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    username = form_data.username
    password = form_data.password
    user = CrudManager.get_user_by_username(db, username)
    if not user:
        raise HTTPException(
            status_code=404, detail=f"Пользователя '{username}' не существует")
    if not hash_manager.verify_password(password_checker=password, password_original=str(user.password)):
        raise HTTPException(status_code=401, detail=f"Не верный пароль")
    token = jwt_manager.create_token(data={"sub": username})
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=1800,
        secure=True,
        samesite='lax',
    )
    # гарантированный способ убать чувствительные поля
    return UserBase.model_validate(user)


@router.get("/logout/", status_code=status.HTTP_200_OK)
def logout_user(response: Response):
    response.delete_cookie(key="access_token")
    ...  # в этой точке нужно внести токен в чёрный список, чтобы пользователь в случае плохих намеренний не использовал их повторно?
    return {"msg": "Вы вышли из системы"}
