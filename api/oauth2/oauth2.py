from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from .. database.database import get_db
from sqlalchemy.orm import Session
from .. validators import val_auth
from jose import JWTError, jwt
from .. models import mdl_users
from .. config import settings


oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')


JWT_SECRET_KEY = settings.JWT_SECRET_KEY
ALGORITHM = settings.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})

    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get('id')
        if not id:
            raise credentials_exception
        token_data = val_auth.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized', headers={'WWW-Authenticate': 'Bearer'})

    token = verify_access_token(token, credentials_exception)
    user = db.query(mdl_users.Users).filter(mdl_users.Users.id == token.id).first()

    return user
