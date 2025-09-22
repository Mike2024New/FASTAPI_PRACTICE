from fastapi import HTTPException, Cookie, Depends
from sqlalchemy.orm import Session
from typing import Annotated
from .BASE.crud import CrudManager
from .BASE.database import get_db
from .security import jwt_manager

# проверка токена пользователя
async def get_user_from_token(db: Annotated[Session, Depends(get_db)], access_token: Annotated[str | None, Cookie()] = None):
    exception_verify = HTTPException(status_code=401, detail="Отказано в доступе, войдите через личный кабинет")
    if access_token is None:
        raise exception_verify
    try:
        payload = jwt_manager.get_payload_from_token_verify(token_in=access_token)
        username = payload.get("sub")
        if username is None:
            raise exception_verify
    except Exception as err:
        print(err)
        raise exception_verify
    user = CrudManager.get_user_by_username(db, username)
    if user is None:
        raise exception_verify