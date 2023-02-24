import contextlib
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session, relationship
from sqlalchemy import Column, func, select
from sqlalchemy import Integer, String, DATETIME, TEXT, ForeignKey,DateTime
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import object_session
from sqlalchemy.orm import column_property

from typing import Generator

import requests
import json
from datetime import datetime

# db初始化
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.testdb"
# 建立操作db引擎
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
# 建立db 模型準備
Base = declarative_base()
# 操作實體類別建立
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 建立表
# 屬性命名要再想一下

# class Apply(Base):
#     __tablename__ = "applys"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#
#     who_apply = Column(String(100))
#     money = Column(Integer)
#
#     title = Column(String(100), ForeignKey('tests.title'))
#     title_relation = relationship("Test", back_populates="apply")
    # Apply_appier_relation = relationship("JoinTest", back_populates="JoinTest_appier_relation", lazy='joined')


class Test(Base):
    __tablename__ = "tests"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100))
    content = Column(TEXT)
    # apply = relationship("Apply", back_populates="title_relation")
    # 這樣會造成n+1問題。
    # @property
    # def apply_count(self):
    #     return object_session(self).query(func.count(Apply.id)).filter(Apply.title==Test.title).scalar()
    # apply_count = column_property(select([func.count(Apply.id)]).where(Apply.title == title))

#
# class JoinTest(Base):
#     __tablename__ = "test_join"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     score = Column(Integer)
#     appier = Column(String(100), ForeignKey(Apply.who_apply))
#     JoinTest_appier_relation = relationship("Apply", back_populates="Apply_appier_relation", lazy='joined')

class Member(Base):
    __tablename__="members"
    id = Column(Integer, primary_key=True, index=True,autoincrement=True,nullable=False,comment="獨立編號")
    name=Column(String,nullable=False,comment="姓名")
    username=Column(String,nullable=False,comment=False)
    password=Column(String,nullable=False,comment="帳戶密碼")
    follower_count=Column(Integer,nullable=False,default=0,comment="追蹤者數量")
    # default跟server_defualt差別在一格用client端產生默認，一個用server端產生默認，這個在time會有差
    time=Column(DateTime(timezone=True),server_default=func.now(),nullable=False,comment="註冊時間")
def create_table():
    Base.metadata.create_all(engine)


def delete_table():
    Base.metadata.drop_all(engine)


# 建立操作實體
# 看起來fastapi 的Depends(get_db)裡面有做到next()
# 透過session 做到available methods (.add(), .query(), .commit(), etc)

@contextlib.contextmanager
def get_db() -> Generator[Session, Session, None]:
    print("start session")
    s = SessionLocal()
    try:
        print("let's start db operation")
        yield s
        s.commit()
        print("gogo db commit")
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()
        print("let's finish this seession")

class Widget(Base):
    __tablename__ = "widget"
    id = Column(Integer, primary_key=True)
    data = Column(Integer)

if __name__ == "__main__":
    def windowed_query(q, column, windowsize):
        """"Break a Query into chunks on a given column."""

        single_entity = q.is_single_entity
        q = q.add_column(column).order_by(column)
        print(q.__dict__)
        print(q)
        last_id = None
        print(124)
        while True:
            subq = q
            if last_id is not None:
                subq = subq.filter(column > last_id)
                print(subq)
            chunk = subq.limit(windowsize).all()
            print("GGGG")
            if not chunk:
                break

            # print(chunk)
            last_id = chunk[-1][-1]
            for row in chunk:
                if single_entity:
                    yield row[0]
                else:
                    yield row[0:-1]
    with get_db() as db:
        # 2.0更新
        db:Session
        # delete_table()
        create_table()
        # 兩種做關聯table方法
        # 1.連結數據物件，直接操作back_populates屬性
        # print(list(enumerate[1,2,3,4]))
        # a=[ (i , j) for i,j in enumerate([1,2,3,4],1)]
        # print(a)



        # get some random list of unique values

        # data = set([random.randint(1, 1000000) for i in range(10000)])
        # db.add_all([Widget(id=i, data=j) for i, j in enumerate(data, 1)])
        # db.commit()
        q = db.query(Widget)
        count=0
        z=Widget.data
        q.add_column(Widget.data).order_by(Widget.data)
        a=q.filter(Widget.id>100).order_by(Widget.id)
        print(a.all())
        # for widget in windowed_query(q, Widget.data, 1000):
        #     count+=1
            # print("data:", widget.data)
        print('DO')
        print(f"total run us {count}")
        # print(result.__dict__)
        # 這邊做的事情就是取出object裡面匹配foreign key的欄位值，填到副表中的foreign key
        # result = db.query(Test).filter(Test.title == "青創指揮部").first()
        # import random
        #
        # # get some random list of unique values
        # data = set([random.randint(1, 1000000) for i in range(10000)])
        #
        #
        # db.add_all([Widget(id=i, data=j) for i, j in enumerate(data, 1)])
        # db.commit()
        # 生成Test假數據
        import string

        # def test(number_of_strings=1, length_of_string=8):
        #     for x in range(number_of_strings):
        #         yield ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string))
        #
        # fake_contents=[Test(content=next(test()),title=next(test())) for _ in range(1000)]
        # db.add_all(fake_contents)
        # db.commit()

        # 生成apply假數據
        # q = db.query(Test).join(Apply)
        # print(q.add_column(Widget.data))
        # for widget in windowed_query(q, Widget.data, 1000):
        #     print("data:", widget.data)
        # for widget in windowed_query(result,)

        # print(result.apply)
        # for a in result.apply:
        #     print(a.who_apply)
        # results=db.query(Apply).filter(Apply.who_apply == 'ford').all()

        # for i in results:
        #     print(i.__dict__)

        # db.commit()

        # print(type(results))
        # for i in results:
        #     i.update(values= {'name':'ford'}, synchronize_session=False)

        # db.add(ford)
        # db.commit()
        # 2.直接打上自己要的
        # Ryuz = Apply(who_apply="Ryuz_lier", money=10000000, title="國家騙錢計畫")
        # print(Ryuz.title_relation)
        # db.add(Ryuz)
        # db.commit()

        # print(result.__dict__)
        #
        # db.commit()
        # db.refresh(ford)
        # delete_table()
        # create_table()
        # url = requests.get("https://sme.moeasmea.gov.tw/startup/upload/opendata/gov_infopack_opendata.json")
        # item = json.loads(url.text)
        # print(item)
        # # 取得的資訊進入db前，先依據定義Table 的title重新命名
        # # 把新建立的資訊，送到表中
        # for i in item:
        #     data_obj = {}
        #     data_obj = {
        #         "title": i["標題"],
        #         "content": i["內容"],
        #         "main_pic": i["主圖"],
        #         "category": i["分類"],
        #         "youtube_iframe": i["youtube嵌入代碼"],
        #         "slide_share": i["slideshare嵌入代碼"],
        #         "publish_time": datetime.strptime(i["建立時間"], "%Y%m%d%H%M%S"),
        #         "update_time": datetime.strptime(i["修改時間"], "%Y%m%d%H%M%S")
        #     }
        #     test_data = Test(**data_obj)  # 拆開用key value送入
        #     # 要存留這次新增的物件row，在Session中使用add()這個函式：
        #     db.add(test_data)
        # db.commit()
        # db.refresh
