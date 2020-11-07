from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from models import users_table, UserInfo, UserInDB, Login
from jose import jwt, JWTError
from typing import Optional, Union
from databases import Database
from passlib.context import CryptContext

from database import connect

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


class Security:
    ACCESS_TOKEN_EXPIRE_MINUTES = 15
    # to get a string like this run:
    # openssl rand -hex 32
    SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM = "HS256"

    def __init__(self, _db: Database):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.db = _db

    def crypt(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    @connect
    async def get_user_by_id(self, user_id: int) -> Union[None, UserInfo]:
        if not user_id:
            return
        get_user_query = users_table.select().where(users_table.c.id == user_id)
        if not (res := await self.db.fetch_one(get_user_query)):
            return
        else:
            return UserInfo(username=res['username'], full_name=res['full_name'], car_model=res['car_model'])

    @connect
    async def get_user_by_username(self, username: str) -> Union[None, UserInfo]:
        if not username:
            return
        get_user_query = users_table.select().where(users_table.c.username == username)
        if not (res := await self.db.fetch_one(get_user_query)):
            return
        else:
            return UserInfo(username=res['username'], full_name=res['full_name'], car_model=res['car_model'])

    @connect
    async def authenticate_user(self, user: Login) -> Union[None, dict]:
        if not user:
            return

        get_user_query = users_table.select().where(users_table.c.username == user.username)
        if not (res := await self.db.fetch_one(get_user_query)) or not self.verify_password(user.password,
                                                                                            res['hashed_password']):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        res = dict(res)
        res.pop('hashed_password')
        return res

    @connect
    async def get_user_by_token(self, token: str = Depends(oauth2_scheme)) -> UserInDB:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        user_query = users_table.select().where(users_table.c.username == username)
        user = await self.db.fetch_one(user_query)
        if user is None:
            raise credentials_exception
        return UserInDB(**user)

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, Security.SECRET_KEY, algorithm=Security.ALGORITHM)
        return encoded_jwt
