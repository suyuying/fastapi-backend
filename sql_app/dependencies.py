# Create, Read, Update, and Delete.
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fastapi import Depends
from jose import JWTError, jwt
from .config import oauth2_scheme, get_settings
from .exception import get_exception_type
from .database.read import get_member_id_email
from .database.database import SessionLocal
from .database.models import Member, Permission
from .schema.dependencies_schema import TokenData



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_token_info(token: str = Depends(oauth2_scheme), settings=Depends(get_settings)):
    # 檢查header是否有sub
    try:
        print(token)
        # 解開token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("sub")
        user_email: str = payload.get("email")
        if user_id is None:
            raise get_exception_type.member_notfound_exception
        if user_email is None:
            raise get_exception_type.email_notfound_exception
        # 這邊都是pydnatic物件 要注意，教學文件有是沒是就會用，因為可以檢查格式
        token_data = TokenData(id=user_id, email=user_email)
        return token_data
    except JWTError:
        raise get_exception_type.credentials_exception


# oauth2_scheme分析進來的request，檢查表頭有沒有帶authorization跟bearer token，沒有報錯，than 取token然後拿裡面的sub值
# 值是None就raise exception ,than
async def get_current_member(db: Session = Depends(get_db), token_data: TokenData = Depends(get_token_info)):
    # 比對db
    # 確定db裡面有username 取東西的方式都適用class.屬性，是因為裡面都用class去溝通
    member = get_member_id_email(db=db, member_id=token_data.id, member_email=token_data.email)
    if member is None:
        raise get_exception_type.credentials_info_exception
    return member


# 拿到class檢查裡面屬性
async def get_current_active_member(current_member: Member = Depends(get_current_member)):
    if current_member.disable:
        raise get_exception_type.member_disalbe_exception
    return current_member


# 因為對於權限要求有很多，ex.可讀可寫這些，因次改用進階版可以帶入參數的depend
# def admin_required(current_active_member: Member = Depends(get_current_active_member)):
#     if not current_active_member.roles_relation.permissions & Permission.ADMIN == Permission.ADMIN:
#         raise get_exception_type.not_authorized_exception
#     return current_active_member

# 因為對於權限要求有很多，ex.可讀可寫這些，因次改用進階版可以帶入參數的depend
# 其實他可以直接在route上面用permission_checker(Permission.ADMIN)直接帶入，不過考量到depend都在dependenices使用
# 所以在這邊直接實作，再用import< 另外depend只能在route上用，一般function不行
class permission_checker:
    def __init__(self, permission_level):
        self.permission_level = permission_level

    def __call__(self, current_active_member: Member = Depends(get_current_active_member)):
        if not current_active_member.roles_relation.permissions & self.permission_level == self.permission_level:
            raise get_exception_type.not_authorized_exception
        return current_active_member


admin_required = permission_checker(Permission.ADMIN)
member_write_required = permission_checker(Permission.WRITE)
