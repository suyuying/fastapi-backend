# Create, Read, Update, and Delete.
from sqlalchemy.orm import Session
from .models import Member, Message
from ..schema.member_schema import MemberCreateInfo

from ..config import Settings

from ..tools import verify_password
from ..exception import get_exception_type
from .read import get_member_username

# 登入的帳密檢查
def authenticate_member(db: Session, user_name: str, password: str, settings: Settings):
    # <sql_app.models.Member object at 0x1107a2cd0>，就算用type hint也不會轉換
    member = get_member_username(db, member_name=user_name)
    if not member:
        raise get_exception_type.member_notfound_exception
    if not verify_password(password, member.password, settings=settings):
        raise get_exception_type.password_wrong_exception
    return member