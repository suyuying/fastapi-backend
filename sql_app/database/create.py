# Create, Read, Update, and Delete.
from sqlalchemy.orm import Session
from ..schema.member_schema import MemberCreateInfo
from ..schema.message_schema import MessageCreateInfo
from ..schema.article_schema import ArticleCreateInfo
from ..tools import get_password_hash
from .models import Member, Message,Role,ArticleCategory,Article
from ..config import Settings,get_settings
from fastapi.encoders import jsonable_encoder



# 這裡要對應到路由那邊的request
def create_member(db: Session, member: MemberCreateInfo, settings: Settings):
    # 更改class裡面的屬性，把密碼加密
    member.password = get_password_hash(member.password,settings=settings)
    # pydantic物件是拿來看body符合，透過dict轉乘python dict後進db
    # 從client端近來都會是pydantic物件，要轉格式才能進db(內建用dict()轉pydantic物件)
    if member.email == get_settings().FLASKY_ADMIN:
        role = db.query(Role).filter_by(name='Administrator').first()
        member_info=Member(**member.dict(),roles_relation=role)
    else:
        role = db.query(Role).filter_by(default=True).first()
        member_info=Member(**member.dict(),roles_relation=role)
    db.add(member_info)
    db.commit()
    db.refresh(member_info)
    # orm_mode =True -> 會自動在response轉orm_model成json,另外如果是路由出去的response出問題，這不影響db資料添加
    return member_info
# create article
def create_article(db: Session, article: ArticleCreateInfo, current_member: Member):
    article_category=db.query(ArticleCategory).filter(ArticleCategory.category==article.category).first()
    article_to_db=article.dict(exclude={'category'})
    article_db=Article(**article_to_db,members_relation=current_member,articleCategory_relation=article_category)

    db.add(article_db)
    db.commit()
    db.refresh(article_db)

    # orm_mode =True -> 會自動轉pydnatic model,另外如果是路由出去的response出問題，這不影響db資料添加
    return article

# create message
def create_message(db: Session, message: MessageCreateInfo, member_table: Member):
    # 用外鍵關聯做出外鍵項目
    message = Message(**message.dict(), member_relation=member_table)  # 要轉換.dict是pydantic->dict
    db.add(message)
    db.commit()
    db.refresh(message)
    # orm_mode =True -> 會自動轉pydnatic model,另外如果是路由出去的response出問題，這不影響db資料添加
    return message


