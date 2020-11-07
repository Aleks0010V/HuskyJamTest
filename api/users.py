from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional, Union
from auth import oauth2_scheme
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt

from models import users_table, tokens_table, roles_table
from database import db


# ==================================================================================
# ================================ models ==========================================
class User(BaseModel):
    username: Optional[str] = ''
    full_name: Optional[str] = ''
    password: Optional[str] = ''
    car_model: Optional[str] = ''


class Login(BaseModel):
    username: str
    password: str


class NewUser(BaseModel):
    username: str
    password: str
    full_name: Optional[str] = ''
    car_model: Optional[str] = ''

# ==================================================================================


# ==================================================================================
# ======================== configuration ===========================================
class Security:
    ACCESS_TOKEN_EXPIRE_MINUTES = 15
    # to get a string like this run:
    # openssl rand -hex 32
    SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM = "HS256"

    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def crypt(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    async def get_user_by_id(user_id: int) -> Union[None, User]:
        if not user_id:
            return
        get_user_query = users_table.select().where(id=user_id)
        if not (res := await db.fetch_one(get_user_query)):
            return
        else:
            return User(username=res['username'], full_name=res['full_name'], car_model=res['car_model'])

    @staticmethod
    async def get_user_by_username(username: str) -> Union[None, User]:
        if not username:
            return
        get_user_query = users_table.select().where(username=username)
        if not (res := await db.fetch_one(get_user_query)):
            return
        else:
            return User(username=res['username'], full_name=res['full_name'], car_model=res['car_model'])

    async def authenticate_user(self, user: Login) -> Union[None, User]:
        if not user:
            return

        get_user_query = users_table.select().where(username=user.username)
        if not (res := await db.fetch_one(get_user_query)) or not self.verify_password(user.password, res['hashed_password']):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return User(username=res['username'], full_name=res['full_name'], car_model=res['car_model'])

    @staticmethod
    async def get_user_by_token(token: str = Depends(oauth2_scheme)) -> Union[None, User]:
        pass

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


router = APIRouter()
security = Security()


@router.on_event("startup")
async def startup():
    await db.connect()
    roles = await db.fetch_all(roles_table.select())
    if not roles:
        query = roles_table.insert().values([{'id': 0, 'role': 'user'},
                                             {'id': 1, 'role': 'master'},
                                             {'id': 2, 'role': 'admin'}]
                                            )
        await db.execute(query)


@router.on_event("shutdown")
async def shutdown():
    await db.disconnect()

# ==================================================================================


@router.post('/create_user')
async def create_user(user: NewUser):
    query = users_table.insert().values(username=user.username,
                                        hashed_password=security.crypt(user.password),
                                        car_model=user.car_model,
                                        full_name=user.full_name,
                                        role_id=0
                                        )
    last_record_id = await db.execute(query)
    return {**user.dict(), "id": last_record_id}


@router.patch('/update_user_info', dependencies=[Depends(Security.get_user_by_token)])
async def update_user_info(user: User, token: str = Depends(oauth2_scheme)):
    pass


@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await security.authenticate_user(Login(username=form_data.username, password=form_data.password))

