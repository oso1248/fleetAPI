from pydantic import BaseModel, conint


class UserLogin(BaseModel):
    eid: str
    password: str


class UserCurrent(BaseModel):
    id: int
    eid: str
    name_first: str
    permissions: conint(ge=0, le=6)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int
    
