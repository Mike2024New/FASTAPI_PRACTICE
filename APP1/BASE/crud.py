from sqlalchemy.orm import Session
from ..BASE.models import User


class CrudManager:
    @staticmethod
    def get_users_all(db: Session):
        return db.query(User).all()

    @staticmethod
    # проверка что пользователь существует
    def get_user_by_username(db: Session, username: str):
        user = db.query(User).filter(User.username == username).first()
        return user

    @staticmethod
    # добавление пользователя в БД
    def add_new_user(db: Session, username: str, password: str):
        user = User(username=username, password=password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @classmethod
    def del_user_by_username(cls, db: Session, username: str):
        user = cls.get_user_by_username(db, username)
        if user:
            db.delete(user)
            db.commit()
        return user
