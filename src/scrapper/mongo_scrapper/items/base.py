from pydantic import BaseModel


class BaseItem(BaseModel):
    index: str
    user: str
    text: str
    number_of_comments: int
    likes: int
