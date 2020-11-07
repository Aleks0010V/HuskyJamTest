from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from typing import Optional, Union
from databases import Database


from models import users_table, roles_table
from auth import oauth2_scheme
from database import db, connect


# ==================================================================================
# ================================ models ==========================================
class UserInfo(BaseModel):
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


class NewUserResponse(BaseModel):
    id: int
    username: str
    full_name: str
    car_model: str


class Token(BaseModel):
    access_token: str
    token_type: str

# ==================================================================================


# ==================================================================================
# ======================== configuration ===========================================
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
    async def get_user_by_token(self, token: str = Depends(oauth2_scheme)):
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
        return user

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
security = Security(db)


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


@router.post('/create_user', response_model=NewUserResponse)
async def create_user(user: NewUser):
    query = users_table.insert().values(username=user.username,
                                        hashed_password=security.crypt(user.password),
                                        car_model=user.car_model,
                                        full_name=user.full_name,
                                        role_id=0
                                        )
    last_record_id = await db.execute(query)
    res = {**user.dict(), "id": last_record_id}
    res.pop('password')
    return res


@router.patch('/update_user_info')
async def update_user_info(info: UserInfo, user: UserInfo = Depends(security.get_user_by_token)):
    pass


@router.post('/login', response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await security.authenticate_user(Login(username=form_data.username, password=form_data.password))
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = security.create_access_token(data={"sub": user['username']}, expires_delta=access_token_expires)
    return {"access_token": token, "token_type": "bearer"}
