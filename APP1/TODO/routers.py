from fastapi import APIRouter, Depends
from ..SECURITY.dependencies import get_user_from_token

router = APIRouter(prefix="/todo", tags=["todo",])

# защита маршрута, только авторизованные пользователи теперь могут попасть сюда
@router.get("/", dependencies=[Depends(get_user_from_token)])
def home():
    return {"msg" : "Приложение todolist"}