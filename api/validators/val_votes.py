from pydantic import BaseModel, UUID4, conint


class VoteBase(BaseModel):
    id_post: int
    dir: conint(ge=0, le=1)
