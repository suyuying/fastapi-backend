# token篇
from datetime import datetime, timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

# 專門用來對password 做hash
from passlib.context import CryptContext
from pydantic import BaseModel

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 測試db
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}

#
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str

# 對password加鹽的物件
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# token跟誰拿，這邊用相對url拿
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


# 驗證加鹽password 跟 plain text 會true
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# 加鹽
def get_password_hash(password):
    return pwd_context.hash(password)

# 把db內的整筆資訊取出，用key value形式放到model中
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        UserInDB(**user_dict)
        return UserInDB(**user_dict)
# 串 get_user()取class
# 比對使用者資料 return class， 驗證有無此user ，且加鹽後的密碼是否跟輸入密碼相同
def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# data來自某user的username(sub是用來辨認用戶） 然後加個有效期 之後加密 return token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# 分析進來的request，檢查表頭有沒有帶authorization跟bearer token，沒有報錯，than 取token然後拿裡面的sub值
# 值是None就raise exception ,than
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user_exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Could not find user",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # 檢查header是否有sub
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username) #這邊都是pydnatic物件 要注意
    except JWTError:
        raise credentials_exception
    # 比對db
    # 確定db裡面有username 取東西的方式都適用class.屬性，是因為裡面都用class去溝通
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise user_exception
    return user

#拿到class檢查裡面屬性
async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# 驗證用戶，創token
# depend串的方式 都是由底往上串，直到頂部之後，取query 等等 之後拿值回到最下面
# 由表格輸的username password去拿token
@app.post("/token", response_model=Token) # 限制response格式 錯了會報錯
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()): # 提示物件 用class做提示 驗證資料是Form帶過來 而且是username and password
    user = authenticate_user(fake_users_db, form_data.username, form_data.password) # 比對db有user名稱 拿user 放到 class 沒有return False
    if not user: # False代表無此帳 回去的報錯照規定要這樣帶
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
 # 做token 回給user
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

# get_current_active_user -> get_current_user _> oauth2_scheme( fastapi secutrity 物件 會去對request內含物有無token）
# 最後拿到的是basemodel extend的class
@app.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]

# 大致流程：
# 1.發 token （使用form做驗證)
# 因為太多人用，所以fastapi有內建model去驗證form，所以用了一個class給他，對form驗證是個depend！
# 找db看有無此username 有就對加鹽密碼 都符合就把db資料撈出來，換成model，之後用username and 過期時間做成token
# 用model優點是可以檢驗格式
#
# 2.登入驗證token
#  先取出client request 的驗證header （depend 物件)
# 解碼取sub，沒有sub就報錯說token有問題，有就進db比資料看有無此user，無就報token有錯，有就把資料取出用model驗正
# 拿折user資料把資源讀出來～
#