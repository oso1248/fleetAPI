from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..validators import val_users, val_auth
from typing import List
from ..models import mdl_users
from ..utils import utils
from ..database.database import get_db
from ..oauth2.oauth2 import get_current_user


router = APIRouter(prefix="/users", tags=['Users'])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=val_users.UsersGet)
def users_create(user: val_users.UsersCreate, db: Session = Depends(get_db)):
    user.password = utils.hash_password(user.password)
    data = mdl_users.Users(**user.dict())
    db.add(data)
    db.commit()
    db.refresh(data)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return data


@router.get("", response_model=List[val_users.UsersGet])
def users_get_all(db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):
    data = db.query(mdl_users.Users).all()
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return data


@router.get("/{id}", response_model=val_users.UsersGet)
def users_get_one(id: int, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):
    data = db.query(mdl_users.Users).filter(mdl_users.Users.id == id).first()
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return data


@router.put("/{id}", response_model=val_users.UsersGet)
def users_update(post: val_users.UsersUpdate, id: int, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):
    data = db.query(mdl_users.Users).filter(mdl_users.Users.id == id)
    if not data.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    data.update(post.dict(), synchronize_session=False)
    db.commit()
    return data.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def posts_delete(id: int, db: Session = Depends(get_db), current_user: val_auth.UserCurrent = Depends(get_current_user)):
    data = db.query(mdl_users.Users).filter(mdl_users.Users.id == id)
    if not data.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    data.delete(synchronize_session=False)
    db.commit()
    return
