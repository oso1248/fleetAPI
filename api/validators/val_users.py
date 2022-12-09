from pydantic import BaseModel, conint
from datetime import datetime


class UsersBase(BaseModel):
    eid: str
    name_first: str
    name_last: str
    is_active: bool = True
    permissions: conint(ge=0, le=6) = 1


class UsersCreate(UsersBase):
    password: str


class UsersGet(UsersBase):
    id: int
    time_created: datetime

    class Config:
        orm_mode = True


class UsersUpdate(BaseModel):
    is_active: bool
    permissions: conint(ge=0, le=6)
