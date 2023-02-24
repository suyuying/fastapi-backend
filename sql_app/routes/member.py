from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ..dependencies import get_current_active_member
from ..schema.member_schema import MemberCreateInfo, MemberUpdateInfo, MemberInfo
from ..database.read import get_member_username, get_member_email, get_members, get_member_id
from ..database.delete import delete_me_member
from ..database.create import create_member
from ..database.models import Member
from ..database.update import update_member
from ..dependencies import get_settings, admin_required
from ..exception import get_exception_type

router = APIRouter(
    prefix="/members",
    tags=["member"]
)


# 新增
@router.post("/")
def create_member_route(member: MemberCreateInfo, db: Session = Depends(get_db),
                        settings = Depends(get_settings)) -> MemberInfo:
    # 檢查username !!
    member_name = get_member_username(db, member.username)
    if member_name is not None:
        raise get_exception_type.member_already_registered_exception
    # 檢查email
    check_email = get_member_email(db, member)
    if check_email is not None:
        raise get_exception_type.email_already_registered_exception
    return create_member(db=db, member=member, settings=settings)

# 取得單一member
@router.get("/me")
def get_member_route(current_member: Member = Depends(get_current_active_member),
                     ) -> MemberInfo:
    # 進db看資料 這邊return orm_model,因為有設定orm_mode所以會自動轉成pydantic
    # 檢查username

    return current_member
# # 取得所有members
@router.get("/all",)
def get_members_route(db: Session = Depends(get_db), skip: int = 0, limit: int = 100,admin=Depends(admin_required)) -> \
list[MemberInfo]:
    # 進db看資料 這邊return orm_model,因為有設定orm_mode所以會自動轉成pydantic
    members = get_members(db=db, skip=skip, limit=limit)
    return members


#
#



#
# 這裡還要再改
# update_member
@router.patch("/me")
def update_member_route(current_member: Member = Depends(get_current_active_member), db: Session = Depends(get_db),
                        update_payload: MemberUpdateInfo = None,settings = Depends(get_settings)) -> MemberInfo | dict:
    # 進db看資料 這邊return orm_model,因為有設定orm_mode所以會自動轉成pydantic
    # member = crud.get_member_username(db=db, member_name=username)
    # # 如果沒撈到東西會return None,而把None直接傳出去是會報錯500的
    # if member is None:
    #     raise HTTPException(status_code=404, detail="user can not find")
    update_result = update_member(db=db, current_member=current_member, update_payload=update_payload,settings=settings)
    return update_result


#
#
# delete member
@router.delete("/me")
def delete_member_route(current_member: Member = Depends(get_current_active_member), db: Session = Depends(get_db)
                        ) -> dict:
    delete_me_member(db=db,current_member=current_member)
    # delete 再去refresh會報錯
    # db.refresh(current_member)
    return {"status": f"{current_member.username} has been deleted"}
