# 待修
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from ..config import get_settings, Settings
from ..dependencies import get_db
from ..dependencies import member_write_required, get_current_active_member
from ..schema.article_schema import ArticleCreateInfo, ArticleGetInfo, ArticleUpdateInfo
from ..database.create import create_article
from ..database.read import get_member_message, get_allmember_message, get_me_articles, get_all_articles
from ..database.delete import delete_me_article
from ..database.update import update_article
from ..database.models import Member, Article, ArticleCategory
from fastapi.encoders import jsonable_encoder

router = APIRouter(
    prefix="/article",
    tags=["article"]
)


# article
@router.post("/")
def create_article_route(article: ArticleCreateInfo, db: Session = Depends(get_db),
                         current_member: Member = Depends(member_write_required)) -> ArticleCreateInfo:
    article = create_article(db=db, article=article, current_member=current_member)
    return article


@router.get("/all")
def get_articles_route(db: Session = Depends(get_db)) -> list[ArticleGetInfo]:
    my_articles_orm = get_all_articles(db=db)

    return my_articles_orm


@router.get("/")
def get_article_route(current_member: Member = Depends(get_current_active_member),
                      db: Session = Depends(get_db)) -> list[ArticleGetInfo]:
    my_articles_orm = get_me_articles(db=db, member_table=current_member)

    return my_articles_orm


@router.delete("/{article_id}/")
def delete_article_route(article_id: int, current_member: Member = Depends(get_current_active_member),
                         db: Session = Depends(get_db)):
    delete_me_article(db=db, article_id=article_id, current_member=current_member)
    return {"status": f"Article number: {article_id} has been deleted"}


@router.patch("/{article_id}/")
def update_article_route(article_id: int, current_member: Member = Depends(get_current_active_member),
                         db: Session = Depends(get_db),
                         update_payload: ArticleUpdateInfo = None,
                         settings: Settings = Depends(get_settings)) :
    # 進db看資料 這邊return orm_model,因為有設定orm_mode所以會自動轉成pydantic
    # member = crud.get_member_username(db=db, member_name=username)
    # # 如果沒撈到東西會return None,而把None直接傳出去是會報錯500的
    # if member is None:
    #     raise HTTPException(status_code=404, detail="user can not find")
    update_result = update_article(article_id=article_id, db=db, current_member=current_member,
                                   update_payload=update_payload,
                                   )
    return update_result
