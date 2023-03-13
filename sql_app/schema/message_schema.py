from pydantic import BaseModel, Field


# message content
class MessageCreateInfo(BaseModel):
    content: str = Field(title="留言")
    article_id:int = Field(title="文章編號")
