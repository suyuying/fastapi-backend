from .utilis import OAuth2PasswordBearerWithCookie
from pydantic import BaseSettings,EmailStr
from passlib.context import CryptContext
from dotenv import load_dotenv,find_dotenv
from functools import lru_cache
from sqlalchemy import create_engine
# 這個oauth2_scheme怎麼整併到settings要再想想，因為它的功能是會檢查token，會牽涉到檢查最後return token，用setting會不知道他在幹嘛
# token跟誰拿，這邊用相對url拿
# *4#vX2GJ9khugM@
import os
class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    # 對password加鹽的物件
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    # sql連線網址
    SQLALCHEMY_DATABASE_URL:str
    TOKENURL:str
    FLASKY_ADMIN :EmailStr
    ARTICLE_CATEGORY=["PythonBasic", "Fastapi", "DataScience", "PythonModule", "LinuxShellScript", "JavaScriptBasic","React"]

    class Config:
        env_file = os.path.join(os.path.dirname(__file__),'.env')
        env_file_encoding = 'utf-8'


# 基本config 壹定要放在這
@lru_cache()
def get_settings():
    return Settings()
oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl=get_settings().TOKENURL)
