# Create, Read, Update, and Delete.
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from .models import Member, Article
from fastapi import HTTPException, Depends
from datetime import datetime, timedelta
from jose import JWTError, jwt
from ..config import Settings, oauth2_scheme
from ..dependencies import get_current_active_member
from ..schema.member_schema import MemberUpdateInfo
from ..schema.article_schema import ArticleUpdateInfo
from ..exception import get_exception_type
from ..tools import get_password_hash
from fastapi.security import OAuth2PasswordBearer


def update_member(db: Session, settings: Settings, update_payload: MemberUpdateInfo,
                  current_member: Member = Depends(get_current_active_member), ):
    if update_payload is None:
        raise get_exception_type.payload_notfound_exception
    # 讓設定為default的值 不換成dict
    update_payload_dict: dict = update_payload.dict(exclude_unset=True)
    if update_payload_dict.get('password') and current_member.password != update_payload_dict.get('password'):
        update_payload_dict['password'] = get_password_hash(update_payload_dict.get('password'), settings=settings)
    db.query(Member).filter(Member.id == current_member.id).update(update_payload_dict,
                                                                   synchronize_session=False)
    db.commit()
    # db.refresh(current_member)
    return {"success":"member has been updated"}


def update_article(article_id: int, db: Session, update_payload: ArticleUpdateInfo,
                   current_member: Member = Depends(get_current_active_member), ):
    if update_payload is None:
        raise get_exception_type.payload_notfound_exception
    # 讓設定為default的值 不換成dict
    update_payload_dict: dict = update_payload.dict(exclude_unset=True)
    aritcle_to_update = db.query(Article).filter(Article.member_id == current_member.id,
                                                 Article.id == article_id).first()
    if aritcle_to_update is None:
        raise get_exception_type.article_notfound_exception
    db.query(Article).filter(Article.member_id == current_member.id,
                             Article.id == article_id).update(update_payload_dict, synchronize_session='fetch')
    db.commit()
    # 這邊如果不refresh，sqlalchemy會因為前值已耕新，導致這邊會拿到空值
    # db.refresh(aritcle_to_update)
    return {"success":"article has been updated"}
