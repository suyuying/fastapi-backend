# 做會員留言系統
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
# from ..dependencies import get_db
from .database import get_db
from ..config import get_settings


class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16


class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, comment="獨立編號")
    name = Column(String, unique=True, nullable=False,index=True)
    default = Column(Boolean, default=False, index=True)
    permissions = Column(Integer,unique=True)
    members_relation=relationship("Member",back_populates="roles_relation")

    def __init__(self, **kwargs):
        # 這邊實際上做啥要再查，查他意思是用父類別的init方法初始化，也就是說子類別會拿到父類別的屬性跟寫在__init__的物件屬性
        # 原本以為這個不用，註解以後會報錯，sqlalchemy.exc.IntegrityError: (sqlite3.IntegrityError) NOT NULL constraint failed: roles.name
        # 看起來是不這樣用就會抓到後來送入Role(name=r)的r值，
        # 目前看起來八成是sqlalchemy有寫特殊的init方法，會把class的東西拿去轉成物件屬性，然後為了要配和db.add所以這樣使用
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    def has_permission(self, perm):
        # 這邊是用二進位運算符處理 要注意
        return self.permissions & perm == perm

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    # !important
    def __repr__(self):
        return '<Role %r>' % self.name

    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.FOLLOW, Permission.COMMENT,Permission.WRITE],
            'Moderator': [Permission.FOLLOW, Permission.COMMENT,
                          Permission.WRITE, Permission.MODERATE],
            'Administrator': [Permission.FOLLOW, Permission.COMMENT,
                              Permission.WRITE, Permission.MODERATE,
                              Permission.ADMIN],
        }
        default_role = 'User'
        db = next(get_db())
        for r in roles:
            role = db.query(Role).filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            # 這裡超重要，roles[r]拿到的是value 也就是那一串list，腦袋到這邊有轉不過來情況！很重要！
            for perm in roles[r]:
                # 這裡會要到permission的class 那便的數值，實際上執行加總數字！
                role.add_permission(perm)
            role.default = (role.name == default_role)

            db.add(role)
        db.commit()


# message關聯 article ,article 關聯member,member 關聯role(final)
# member資料表
class Member(Base):
    __tablename__ = "members"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False, comment="獨立編號")
    name = Column(String, nullable=False, comment="姓名")
    username = Column(String, nullable=False, comment=False, unique=True, index=True)
    password = Column(String, nullable=False, comment="帳戶密碼")
    # EmailStr很特別，他套件是很健全的驗證信箱制度，包含確認是否有該email,regex等，可以研究
    email = Column(String, nullable=False, comment="信箱", unique=True, index=True)
    follower_count = Column(Integer, nullable=False, default=0, comment="追蹤者數量")
    # default跟server_defualt差別在一格用client端產生默認，一個用server端產生默認，這個在time會有差
    disable = Column(Boolean, nullable=False, default=False)
    time = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, comment="註冊時間")
    introduction = Column(String, nullable=False, server_default="hello world", comment="自我介紹")
    articles_relation = relationship('Article', back_populates="members_relation")
    # 後來不用這個寫法，直接寫死permissions會在後續有修改各role的permissions
    roles_permissions=Column(Integer,ForeignKey(Role.id))
    roles_relation=relationship("Role", back_populates="members_relation")
    # 這邊這個設定方法有待商榷
    # def __init__(self, **kwargs):
    #     super(Member, self).__init__(**kwargs)
    #     self.role=None
    #     db = next(get_db())
    #     if self.role is None:
    #         if self.email == get_settings().FLASKY_ADMIN:
    #             self.role = db.query(Role).filter_by(name='Administrator').first()
    #             self.role_permissions=self.role.permissions
    #         if self.role is None:
    #             self.role = db.query(Role).filter_by(default=True).first()
    #             self.role_permissions = self.role.permissions


class ArticleCategory(Base):
    __tablename__ = "articleCategory"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False, comment="文章分類")
    category = Column(String, unique=True, nullable=False, comment="類標題")
    time = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, comment="分類創建時間")
    articles_relation = relationship("Article", back_populates="articleCategory_relation")
    def __init__(self, **kwargs):
        # 這邊實際上做啥要再查，查他意思是用父類別的init方法初始化，也就是說子類別會拿到父類別的屬性跟寫在__init__的物件屬性
        # 原本以為這個不用，註解以後會報錯，sqlalchemy.exc.IntegrityError: (sqlite3.IntegrityError) NOT NULL constraint failed: roles.name
        # 看起來是不這樣用就會抓到後來送入Role(name=r)的r值，
        # 目前看起來八成是sqlalchemy有寫特殊的init方法，會把class的東西拿去轉成物件屬性，然後為了要配和db.add所以這樣使用
        super(ArticleCategory, self).__init__(**kwargs)
    @staticmethod
    def insert_category():
        categories = get_settings().article_category
        db = next(get_db())
        for r in categories:
            category = db.query(ArticleCategory).filter_by(category=r).first()
            if category is None:
                category = ArticleCategory(category=r)
                db.add(category)
                continue
            # 這裡超重要，roles[r]拿到的是value 也就是那一串list，腦袋到這邊有轉不過來情況！很重要！
        db.commit()

class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False, comment="文章獨立編號")
    title = Column(String, nullable=False, comment="標題")

    body = Column(String, nullable=False, comment="內文")
    # default跟server_defualt差別在一格用client端產生默認，一個用server端產生默認，這個在time會有差
    create_time = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, comment="創建時間")
    update_time = Column(DateTime(timezone=True), nullable=True, comment="修改時間")
    member_id = Column(String, ForeignKey(Member.id, ondelete='CASCADE', onupdate='CASCADE'), comment="創建者id")
    members_relation = relationship("Member", back_populates="articles_relation", foreign_keys=[member_id])
    articleCategory_id = Column(String, ForeignKey(ArticleCategory.id), comment="類別id")
    articleCategory_relation = relationship("ArticleCategory", back_populates="articles_relation",
                                            foreign_keys=[articleCategory_id])
    # 對應的主鍵，被刪除或更改時，他的foreingn key也要一起更改
    messages_relation = relationship("Message", back_populates="articles_relation")


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False, comment="獨立編號")
    content = Column(String, nullable=False, comment="留言內容")
    # default跟server_defualt差別在一格用client端產生默認，一個用server端產生默認，這個在time會有差
    time = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, comment="留言時間")
    article_id = Column(String, ForeignKey(Article.id, ondelete='CASCADE', onupdate='CASCADE'))
    articles_relation = relationship("Article", back_populates="messages_relation")
# 更新messages, articles,articlecategory
# body=Column(String,nullable=False,comment="內文")
# # default跟server_defualt差別在一格用client端產生默認，一個用server端產生默認，這個在time會有差
# time=Column(DateTime(timezone=True),server_default=func.now(),nullable=False,comment="創建時間")
# member_id=Column(String,ForeignKey(Member.id),comment="創建者id")
# member_relation=relationship("Member",back_populates="member_messages",foreign_keys=[member_id])


#
# class User(Base):
#     __tablename__ = "users"
#
#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String, unique=True, index=True)
#     hashed_password = Column(String)
#     is_active = Column(Boolean, default=True)
#
#     items = relationship("Item", back_populates="owner")
#
# #表
# class Item(Base):
#     __tablename__ = "items"
#     #列
#     # 參數 SQLAlchemy “类型”，如Integer、String和Boolean，數據庫column數據類型
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     description = Column(String, index=True)
#     owner_id = Column(Integer, ForeignKey("users.id"))
#     # 關係：該表與其他相關表中的值，用來讓foreign直取用更方便
#     # 以下意思是，會指向User model的primary key，back_populates是指items這張表
#     # 整個意思就是，Item model的items表的owner列的值設定foreign key User，這是跟User表的primary key那ㄧ列有關
#     owner = relationship("User", back_populates="items")
