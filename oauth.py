from datetime import timedelta, datetime

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

import schemas as _schemas
import database as _database
import config as _config
import models as _models
import utils as _utils


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')

SECRET_KEY = _config.SECRET_KEY
ALGORITHM = _config.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = _config.ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(data: dict, expires_delta: timedelta or None = None): # type: ignore
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



