import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sql_base_url = os.path.dirname(__file__)
sql_base_url = os.path.join(sql_base_url, "my_base.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{sql_base_url}"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# создание зависимости для маршрутов
def get_db():
    with SessionLocal() as db:
        yield db
