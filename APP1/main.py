from fastapi import FastAPI
from .BASE.models import BASE
from .BASE.database import engine
from .ROUTERS import users, notes

"""
uvicorn APP1.main:app --reload --host 127.0.0.1 --port 8000
http://127.0.0.1:8000/
http://127.0.0.1:8000/docs/
http://127.0.0.1:8000/redoc/
"""

BASE.metadata.create_all(bind=engine)  # создание таблиц (если они ещё не были созданы)
app = FastAPI()
app.include_router(users.router)  # подключение маршрутов с аккаунтами пользователей
app.include_router(notes.router)  # подключение маршрутов с заметками (зависит от аккаунтов пользователей)


@app.get("/", tags=["main"])
def home():
    return {"msg": "Главная страница"}
