from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator
from typing import Annotated
from string import ascii_letters, punctuation, digits, ascii_lowercase

# символы которые допускается использовать в пароле и в логине:
# abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~0123456789
allow_simbols_for_login_password = ascii_letters + punctuation + digits


class UserBase(BaseModel):
    """Публичная модель (не содержит чувствительных данных)"""
    username: Annotated[str, Field(min_length=2, max_length=50)]
    model_config = ConfigDict(json_schema_extra={"examples": [
        {"username": "Иван"}
    ]})


class UserCreate(UserBase):
    """Модель для создания (POST)/полного обновления (PUT) пользователя, содержит чувствительные данные, валидируется
    на входе"""
    password: Annotated[str, Field(description=f"Введите пароль используя символы {allow_simbols_for_login_password}")]
    password_repeat: Annotated[str, Field(description=f"Введите пароль используя символы {allow_simbols_for_login_password}")]
    model_config = ConfigDict(json_schema_extra={"examples": [
        {"username": "Ivan@25", "password": "qwerty1234@", "password_repeat": "qwerty1234@"}
    ]})

    @field_validator("username", mode="after")
    @classmethod
    def check_login_and_password_correct_input(cls, value):
        if not all(i in allow_simbols_for_login_password for i in value):
            raise ValueError(f"Логин должен состоять из символов {allow_simbols_for_login_password}")
        return value

    @field_validator("password", "password_repeat", mode="after")
    @classmethod
    def check_password(cls, value):
        error_list = []
        if len(value) < 8:
            error_list.append(f"Пароль должен быть длиной не менее 8 символов")
        if len(value) > 50:
            error_list.append(f"Пароль должен быть длиной не более 50 символов")
        if not any(i in allow_simbols_for_login_password for i in value):
            error_list.append(f"Пароль должен состоять из символов {allow_simbols_for_login_password}")
        if not any(i in ascii_lowercase for i in value):
            error_list.append(f"В пароле должна быть хотябы одна заглавная латинская буква {ascii_lowercase}")
        if not any(i in digits for i in value):
            error_list.append(f"В пароле должна быть хотябы одна цифра {digits}")
        if not any(i in punctuation for i in value):
            error_list.append(f"В пароле должен быть хотя бы один символ {punctuation}")
        if error_list:
            error_msg = "\n\t-".join(error_list)
            error_msg = "Не верный ввод пароля:\n" + error_msg
            raise ValueError(error_msg)
        return value

    @model_validator(mode="after")
    def check_passwords_match(self):
        if self.password != self.password_repeat:
            raise ValueError("Пароли не совпадают")
        return self
