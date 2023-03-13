from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ..dependencies import get_current_active_member
from ..schema.message_schema import MessageCreateInfo
from ..database.create import create_message
from ..database.read import get_member_message, get_allmember_message,get_article_message
from ..database.models import Member

router = APIRouter(
    prefix="/message",
    tags=["message"]
)


# create message
@router.post("/")
def create_message_route(message: MessageCreateInfo, db: Session = Depends(get_db),
                         current_member: Member = Depends(get_current_active_member),):
    return create_message(db=db, message=message)


@router.get("/all")
def allmember_messages_route(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_allmember_message(skip=skip, limit=limit, db=db)


# @router.get("/")
# def get_member_message(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
#                        current_member: Member = Depends(get_current_active_member)):
#     return get_member_message(db=db, member_table=current_member, skip=skip, limit=limit)
@router.get("/")
def get_article_message_route(article_id:int,skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
                       ):
    return get_article_message(db=db, article_id=article_id, skip=skip, limit=limit)
