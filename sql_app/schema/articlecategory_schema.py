from pydantic import BaseModel, Field, constr, EmailStr
from datetime import datetime

class ArticleCategoryBase(BaseModel):
    # 這邊Field裡面打default=str會直接報錯，這個bug有點難解。可以去看官網
    # 檢討： 從最底層檢查
    # name: str = Field( title="your true name", max_length=30)
    category: str = Field(title="your category name", min_length=2, max_length=30)


