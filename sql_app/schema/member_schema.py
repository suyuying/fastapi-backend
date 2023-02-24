from pydantic import BaseModel, Field, constr, EmailStr
from datetime import datetime


# member
class MemberBase(BaseModel):
    # 這邊Field裡面打default=str會直接報錯，這個bug有點難解。可以去看官網
    # 檢討： 從最底層檢查
    # name: str = Field( title="your true name", max_length=30)
    name: str = Field(title="your true name", min_length=2, max_length=30)
    username: constr(regex="[a-zA-Z0-9]{2,20}", strip_whitespace=True, max_length=20,
                     min_length=2)

    class Config:
        orm_mode = True


class MemberUpdateInfo(BaseModel):
    # name: str = Field(title="your true name", min_length=2, max_length=30)
    username: constr(regex="[a-zA-Z0-9]{2,20}", strip_whitespace=True, max_length=20,
                     min_length=2) | None = None
    email: EmailStr | None = None
    password: constr(regex="^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@_-]).{8,20}", strip_whitespace=True, max_length=20,
                     min_length=8) | None = None
    time: datetime | None = None


class MemberCreateInfo(MemberBase):
    # 含有數字 英文大小寫 最短8最長20
    # password: str
    email: EmailStr
    password: constr(regex="^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@_-]).{8,20}", strip_whitespace=True, max_length=20,
                     min_length=8)


class MemberInfo(MemberBase):
    roles_permissions: int
    id: int
    email: EmailStr
    follower_count: int | None = None
    time: datetime | None = None
    disable: bool | None = False
    # 這邊沒加orm_mode
