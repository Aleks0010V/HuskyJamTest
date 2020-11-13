from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt, JWTError
from typing import Optional, Union
from passlib.context import CryptContext

from database.database import connect, db
from database.models import UserInfo, UserInDB, Login
from database.schemas import users_table

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


class Security:
    ACCESS_TOKEN_EXPIRE_MINUTES = 15
    # to get a string like this run:
    # openssl rand -hex 32
    SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM = "HS256"
    db = db
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    def crypt(password: str) -> str:
        return Security.pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return Security.pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    @connect
    async def get_user_by_id(user_id: int) -> Union[None, UserInfo]:
        if not user_id:
            return
        get_user_query = users_table.select().where(users_table.c.id == user_id)
        if not (res := await Security.db.fetch_one(get_user_query)):
            return
        else:
            return UserInfo(username=res['username'], full_name=res['full_name'], car_model=res['car_model'])

    @staticmethod
    @connect
    async def get_user_by_username(username: str) -> Union[None, UserInfo]:
        if not username:
            return
        get_user_query = users_table.select().where(users_table.c.username == username)
        if not (res := await Security.db.fetch_one(get_user_query)):
            return
        else:
            return UserInfo(username=res['username'], full_name=res['full_name'], car_model=res['car_model'])

    @staticmethod
    @connect
    async def authenticate_user(user: Login) -> Union[None, dict]:
        if not user:
            return

        get_user_query = users_table.select().where(users_table.c.username == user.username)
        if not (res := await Security.db.fetch_one(get_user_query)) or not Security.verify_password(user.password,
                                                                                            res['hashed_password']):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        res = dict(res)
        res.pop('hashed_password')
        return res

    @staticmethod
    @connect
    async def get_user_by_token(token: str = Depends(oauth2_scheme)) -> UserInDB:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, Security.SECRET_KEY, algorithms=[Security.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:  # check that such user exists
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        user_query = users_table.select().where(users_table.c.username == username)
        user = await db.fetch_one(user_query)
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


async def check_admin_role(user: UserInDB = Depends(Security.get_user_by_token)):
    forbidden_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="admins-only endpoint",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if user.role_id != 2:
        raise forbidden_exception
    else:
        return user
