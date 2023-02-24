# Create, Read, Update, and Delete.
from datetime import datetime, timedelta
from jose import jwt
from .config import get_settings
from fastapi import Depends


#直接用depend會報錯AttributeError: 'Depends' object has no attribute 'SECRET_KEY'
# 原因是不能再own function直接用depends, 只能在routes上面
# password加鹽

def get_password_hash(password, settings =Depends(get_settings)):
    return settings.pwd_context.hash(password)


# 驗證加鹽password 跟 plain text 會true
def verify_password(plain_password, hashed_password, settings =Depends(get_settings) ):
    return settings.pwd_context.verify(plain_password, hashed_password)


# data來自某user的username(sub是用來辨認用戶） 然後加個有效期 之後加密 return token
def create_access_token(data: dict, expires_delta: timedelta | None = None,settings =Depends(get_settings) ):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


