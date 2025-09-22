from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer

BASE = declarative_base()


class User(BASE):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
