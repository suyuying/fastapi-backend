# Create, Read, Update, and Delete.

from fastapi import Depends
from .models import Member, Article
from ..dependencies import get_current_active_member
from sqlalchemy.orm import Session
from ..exception import get_exception_type


def delete_me_member(db: Session, current_member: Member):
    member_will_delete = db.query(Member).filter(Member.id == current_member.id,
                                                 Member.email == current_member.email).first()
    db.delete(member_will_delete)
    db.commit()
    return True


def delete_me_article(db: Session, current_member: Member, article_id: int):
    article_will_delete = db.query(Article).filter(current_member.id == Article.member_id,
                                                   Article.id == article_id).first()
    if article_will_delete is None:
        raise get_exception_type.article_notfound_exception
    db.delete(article_will_delete)
    db.commit()
    return True
