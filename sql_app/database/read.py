# Create, Read, Update, and Delete.
from sqlalchemy.orm import Session
from .models import Member, Message, Article
from ..schema.member_schema import MemberCreateInfo

from ..config import Settings

from ..tools import verify_password
from ..exception import get_exception_type
from sqlalchemy.orm import joinedload


def get_member_id_email(db: Session, member_id: int, member_email: str):
    return db.query(Member).filter(Member.id == member_id, Member.email == member_email).first()


# member
def get_member_email(db: Session, member_email: MemberCreateInfo):
    result = db.query(Member).filter(Member.email == member_email.email).first()
    return result


def get_members(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Member).offset(skip).limit(limit).all()


def get_member_username(db: Session, member_name: str):
    result = db.query(Member).filter(Member.username == member_name).first()
    return result


def get_member_id(db: Session, member_id: int):
    result = db.query(Member).filter(Member.id == member_id).first()
    return result


def get_allmember_message(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Message).offset(skip).limit(limit).all()


def get_member_message(db: Session, member_table: Member, skip: int = 0, limit: int = 100):
    return db.query(Message).filter(Message.member_id == member_table.id).offset(skip).limit(limit).all()


# article
def get_all_articles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Article).offset(skip).limit(limit).all()


def get_me_articles(db: Session, member_table: Member, skip: int = 0, limit: int = 100):
    return db.query(Article).filter(
        Article.member_id == member_table.id).offset(skip).limit(limit).all()
