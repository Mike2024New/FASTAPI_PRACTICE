from fastapi import FastAPI

from .SECURITY.ROUTERS import sign_in
from .SECURITY.BASE.models import BASE as SECURITY_BASE # подключение базы данных с пользователями
from .SECURITY.BASE.database import engine
from .SECURITY.ROUTERS import sign_up
from .TODO import routers as todo
from contextlib import asynccontextmanager

"""
uvicorn APP1.main:app --reload --host 127.0.0.1 --port 8000
http://127.0.0.1:8000/
http://127.0.0.1:8000/docs/
http://127.0.0.1:8000/redoc/
"""


@asynccontextmanager
async def on_startup(application: FastAPI):
    SECURITY_BASE.metadata.create_all(bind=engine)  # создание таблиц (если они ещё не были созданы)
    yield


app = FastAPI(lifespan=on_startup)
app.include_router(sign_up.router)  # модуль с регистрацией пользователей (создание аккаунтов)
app.include_router(sign_in.router) # модуль авторизацией пользователей
app.include_router(todo.router) # подключение приложения


@app.get("/", tags=["main"])
def home():
    return {"msg": "Главная страница"}
