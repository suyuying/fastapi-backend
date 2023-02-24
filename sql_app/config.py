from .utilis import OAuth2PasswordBearerWithCookie
from pydantic import BaseSettings
from passlib.context import CryptContext

from functools import lru_cache

# 這個oauth2_scheme怎麼整併到settings要再想想，因為它的功能是會檢查token，會牽涉到檢查最後return token，用setting會不知道他在幹嘛
# token跟誰拿，這邊用相對url拿
oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="token")


class Settings(BaseSettings):
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    # 對password加鹽的物件
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    # sql連線網址
    SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
    tokenUrl = "token"
    FLASKY_ADMIN = "z0952657360@gmail.com"
    article_category = ['PythonBasic', 'Fastapi', 'DataScience', 'PythonModule', 'LinuxShellScript', 'JavaScriptBasic',
                        'React']

# 基本config 壹定要放在這
@lru_cache()
def get_settings():
    return Settings()
