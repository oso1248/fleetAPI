from fastapi import status, HTTPException, Depends, APIRouter
from ..validators import val_votes, val_auth
from ..oauth2.oauth2 import get_current_user
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..models import mdl_post


router = APIRouter(prefix="/votes", tags=['Votes'])


@router.post("", status_code=status.HTTP_201_CREATED)
def vote(vote: val_votes.VoteBase, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):
    query = db.query(mdl_post.Votes).filter(mdl_post.Votes.id_post == vote.id_post, mdl_post.Votes.id_user == current_user.id)
    is_vote = query.first()
    is_post = db.query(mdl_post.Post).filter(mdl_post.Post.id == vote.id_post).first()

    if not is_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    elif vote.dir == 1 and is_vote:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    elif vote.dir == 1 and not is_vote:
        data = mdl_post.Votes(id_post=vote.id_post, id_user=current_user.id)
        db.add(data)
        db.commit()
    elif not is_vote:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        query.delete(synchronize_session=False)
        db.commit()
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)

    return
