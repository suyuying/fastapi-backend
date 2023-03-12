from pydantic import BaseModel, Field, ValidationError
from typing import Literal, Union
from datetime import datetime
from ..config import get_settings
article_category=get_settings().ARTICLE_CATEGORY

class ArticleCategory_relation(BaseModel):
    category: str
    time:datetime
    class Config:
        orm_mode = True
class Members_relation(BaseModel):
    username:str
    follower_count:int
    class Config:
        orm_mode = True

class ArticleBase(BaseModel):
    title:str|None =Field(default="hello")
    body:str|None=Field(default=None)
    class Config:
        orm_mode = True
class ArticleCreateInfo(ArticleBase):
    # 限制類別須在定義的article_category內，不包含會報錯
    category : Literal[*article_category]
    pass

class ArticleGetInfo(ArticleBase):
    id:int
    update_time:datetime|None=None
    create_time:datetime|None=None
    articleCategory_relation:ArticleCategory_relation|None=None
    members_relation:Members_relation


class ArticleUpdateInfo(ArticleBase):
    update_time:datetime=Field(default=datetime.now())
    # category: Literal[*article_category]