from fastapi import FastAPI,Depends
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from datetime import datetime

app = FastAPI()


class TestInPut(BaseModel):
    user_name: str
    email: str | None =None
    password: int | None=None
    # time: datetime.now()

class TestOutPut(BaseModel):
    user_name:str
    email:str
    time:str
    q:str
    skip:int


# def helloworld(q:str,skip:int=0):
#     return {'q':q,'skip':skip}
class helloworld:
    def __init__(self, q: str | None = None, skip: int = 0):
        self.q = q
        self.skip = skip
def hello_des_depend(is_depend:str)->str:
    return is_depend

def hellodes(hinan:str= Depends(hello_des_depend))->str:
    print(hinan)
    return hinan
@app.post("/test/{hi}/")
async def test(*,hello:helloworld =Depends(),register_form:TestInPut,hi:str=Depends(hellodes)) -> TestOutPut:
    print(hi)
    print(type(register_form))
    # print(**register_form.dict()) #會報錯
    for k,v in register_form.dict().items():
        print(k,v)
        print(type(v))
    print(register_form.dict())
    register_form_dict=register_form.dict()
    register_form_dict.update({"time":datetime.now()})
    print('++++++')
    register_form_dict.update({'q':hello.q,'skip':hello.skip})
    for k,v in jsonable_encoder(register_form_dict).items():
        print(k,v)
        print(type(v))
    return jsonable_encoder(register_form_dict)
# from fastapi import Depends, FastAPI
#
# app = FastAPI()
#
#
# fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
#
#
# class CommonQueryParams:
#     def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
#         self.q = q
#         self.skip = skip
#         self.limit = limit
#
#
# @app.get("/items/")
# async def read_items(commons: CommonQueryParams = Depends()):
#     response = {}
#     if commons.q:
#         response.update({"q": commons.q})
#     print(response)
#     print(commons)
#     # list切片值。恩 很久沒這樣用了zzzz 不過在切分頁資料好用的樣子，list包dict 然後拿到筆數
#     items = fake_items_db[commons.skip : commons.skip + commons.limit]
#     print(items)
#     response.update({"items": items})
#     print(response)
#     return response