from pydantic import BaseModel, UUID4
from datetime import datetime
from ..validators.val_users import UsersGet


class PostBase(BaseModel):
    title: str
    content: str
    is_published: bool = True


class PostCreate(PostBase):
    pass


class PostReturn(PostBase):
    id: int
    uuid: UUID4
    time_created: datetime
    creator: UsersGet

    class Config:
        orm_mode = True


class PostGet(BaseModel):
    Post: PostReturn
    votes: int

    class Config:
        orm_mode = True


class PostUpdate(PostBase):
    is_published: bool
