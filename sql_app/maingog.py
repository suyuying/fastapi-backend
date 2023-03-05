from fastapi import FastAPI,Depends,File, UploadFile,Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
# import要有順序，不然會產生引用錯誤(ex 我引用你 你引用我)
# 依賴順序utilis(完全獨立於config)->config->tools(依賴config)->database->dependencies
from .config import get_settings
from .tools import create_access_token

from .database import database,models,create,read,update,delete
from .database.db_tools import authenticate_member
from .dependencies import get_db,admin_required
import aiofiles

from .routes import message,member,article
from .schema.dependencies_schema import Token
from datetime import timedelta
from fastapi.middleware.cors import CORSMiddleware

# 規劃是可以用token.id去查詢資料，登入token用id檢查
# 建立資料表 沒建立會去建立
# database.Base.metadata.drop_all(bind=database.engine)

database.Base.metadata.create_all(bind=database.engine)
control_insert_role=False
if not control_insert_role:
    models.Role.insert_roles()
    control_insert_role=True
# 掃table，確認現在是否有所需欄位，沒有建立，有就continue
models.ArticleCategory.insert_category()
app = FastAPI()
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost:3000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(message.router)
app.include_router(member.router)
app.include_router(article.router)


@app.post("/token", response_model=Token)  # 限制response格式 錯了會報錯
async def login_for_access_token(response: Response,form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db),
                                 settings = Depends(
                                     get_settings)):  # 提示物件 用class做提示 驗證資料是Form帶過來 而且是username and password
    user = authenticate_member(db, form_data.username, form_data.password,settings=settings)  # 比對db有user名稱 拿user 放到 class 沒有return False

    # 做token 回給user
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        # sub不是str會報錯，所以先轉str
        settings=settings,data={"sub": str(user.id), "email": user.email}, expires_delta=access_token_expires
    )
    response.set_cookie(key="access_token",value=f"Bearer {access_token}",httponly=True,samesite="none",secure=True)
    return {"access_token": access_token, "token_type": "bearer"}
@app.post("/test",dependencies=[Depends(admin_required)])  # 限制response格式 錯了會報錯
async def test_Admin():  # 提示物件 用class做提示 驗證資料是Form帶過來 而且是username and password
    return 123
@app.post("/files/")
async def create_file(file: bytes = File(description="A file read as bytes")):
    return {"file_size": len(file)}
#
# async def upload_generator(files: list[UploadFile]| None = File(default=None,description="A file read as UploadFile")):
#     if not files:
#         yield {"message": "No upload file sent"}
#     for file in files:
#         try:
#             contents = await file.read()
#             async with aiofiles.open(file.filename, 'wb') as f:
#                 await f.write(contents)
#             yield file.filename
#         except Exception:
#             yield {"message": "There was an error uploading the file"}
#         finally:
#             await file.close()
# @app.post("/uploadfile/")
# async def create_upload_file(
#     files: list[UploadFile]| None = File(default=None,description="A file read as UploadFile"),
# ):
#     for each_upload in upload_generator(files=files):
#         pass






#
# # 新增
# @app.post("/members/", response_model=schemas.Member)
# def create_member(member: schemas.MemberCreate, db: Session = Depends(get_db)):
#
#     # 檢查username !!
#     member_name=crud.get_member_username(db, member.username)
#     if member_name is not None:
#         raise HTTPException(status_code=400, detail="username already registered")
#     # 檢查email
#     check_email = crud.get_member_email(db, member)
#     if check_email is not None:
#         raise HTTPException(status_code=400, detail="email already registered")
#     return crud.create_member(db=db, member=member)
#
# # 取得所有members
# @app.get("/members/")
# def get_members(db: Session = Depends(get_db), skip: int = 0, limit: int = 100) -> list[schemas.Member]:
#     # 進db看資料 這邊return orm_model,因為有設定orm_mode所以會自動轉成pydantic
#     members = crud.get_members(db=db, skip=skip, limit=limit)
#     return members
# # 取得單一member
# @app.get("/members/me")
# def get_member(current_member:models.Member=Depends(get_current_active_user), db: Session = Depends(get_db)) -> schemas.Member:
#     # 進db看資料 這邊return orm_model,因為有設定orm_mode所以會自動轉成pydantic
#     # 檢查username
#     member=crud.get_member_id(db,current_member.id)
#     if member is None:
#         raise HTTPException(status_code=404,detail="member not found")
#     return member
#
# # update_member
# @app.patch("/members/me")
# def update_member(current_member:models.Member=Depends(get_current_active_user), db: Session = Depends(get_db), update_payload:schemas.MemberUpdateSchema=None)-> schemas.Member|dict:
#     # 進db看資料 這邊return orm_model,因為有設定orm_mode所以會自動轉成pydantic
#     # member = crud.get_member_username(db=db, member_name=username)
#     # # 如果沒撈到東西會return None,而把None直接傳出去是會報錯500的
#     # if member is None:
#     #     raise HTTPException(status_code=404, detail="user can not find")
#     update_result=crud.update_member(db=db, current_member=current_member, update_payload=update_payload)
#     if not update_result:
#         return {"status":"you don't input anything to change"}
#     db.refresh(current_member)
#     return crud.get_member_id(db=db, member_id=current_member.id)
#
#
# # delete member
# @app.delete("/member/me")
# def delete_member(current_member:models.Member=Depends(get_current_active_user),db: Session = Depends(get_db)) :
#     db.delete(current_member)
#     db.commit()
#     # delete 再去refresh會報錯
#     # db.refresh(current_member)
#     return {"status": f"{current_member.username} has been deleted"}
#
# #message
#
# # create message
# @app.post("/message/")
# def create_message(message: schemas.MessageCreate, db: Session = Depends(get_db), current_member:models.Member=Depends(get_current_active_user)):
#     return crud.create_message(db=db,message=message,member_table=current_member)
# @app.get("/message/all")
# def all_member_messages(skip: int = 0, limit: int = 100,db: Session = Depends(get_db)):
#     return crud.get_allmember_message(skip=skip, limit=limit, db=db)
# @app.get("/message/")
# def get_member_message(skip: int = 0, limit: int = 100,db: Session = Depends(get_db),current_member:models.Member=Depends(get_current_active_user)):
#     return crud.get_member_message(db=db,member_table=current_member,skip=skip,limit=limit)
#
#
# # # 沒有註明depends ,fastapi會直接報錯fastapi.exceptions.FastAPIError: Invalid args for response field!
# # @app.get("/token") # 限制response格式 錯了會報錯
# # def login_for_access_token(form_data:str,db:Session= Depends(get_db),): # 提示物件 用class做提示 驗證資料是Form帶過來 而且是username and password
# #     return {"status": f" has been deleted"}
# @app.post("/token", response_model=schemas.Token) # 限制response格式 錯了會報錯
# async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),db:Session=Depends(get_db),settings: Settings = Depends(get_settings)): # 提示物件 用class做提示 驗證資料是Form帶過來 而且是username and password
#     user = crud.authenticate_member(db, form_data.username, form_data.password) # 比對db有user名稱 拿user 放到 class 沒有return False
#
#     if not user: # False代表無此帳 回去的報錯照規定要這樣帶
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#  # 做token 回給user
#     access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = crud.create_access_token(
#         # sub不是str會報錯，所以先轉str
#         data={"sub": str(user.id),"email":user.email}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}

# get messages
# update message
# delete message


# @app.post("/users/", response_model=schemas.User)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return crud.create_user(db=db, user=user)
#
#
# @app.get("/users/", response_model=list[schemas.User])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users
#
#
# @app.get("/users/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user
#
#
# @app.post("/users/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(
#         user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)
#
#
# @app.get("/items/", response_model=list[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items
#
#
# @app.post("/test/")
# def for_test(test: schemas.ForTest) -> schemas.ForTest:
#     return test
