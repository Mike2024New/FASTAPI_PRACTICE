import os
from datetime import timedelta
from UTILS.HASH_MANAGER import HashManager
from UTILS.JWT_MANAGER import JWTManager

FASTAPI_SECRET_KEY_FOR_PSW = str(os.getenv("FASTAPI_SECRET_KEY_FOR_PSW"))
FASTAPI_SECRET_KEY_FOR_TOKEY = str(os.getenv("FASTAPI_SECRET_KEY_FOR_TOKEY"))
hash_manager = HashManager(secret_key=FASTAPI_SECRET_KEY_FOR_PSW) # хеширование паролей
jwt_manager = JWTManager(secret_key=FASTAPI_SECRET_KEY_FOR_TOKEY, token_action=timedelta(minutes=30)) # создание jwt токенов