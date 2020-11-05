from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional, Union
from auth import oauth2_scheme
from passlib.context import CryptContext

from models import users_table, tokens_table, roles_table
from database import db


# ==================================================================================
# ================================ models ==========================================
class User(BaseModel):
    username: str
    password: Optional[str] = ''
    car_model: Optional[str] = ''


class NewUser(BaseModel):
    username: str
    password: str
    car_model: str


class ChangePass(BaseModel):
    username: str
    password: str


class ChangeCarModel(BaseModel):
    username: str
    car_model: str
# ==================================================================================


# ==================================================================================
# ======================== configuration ===========================================
class Security:
    ACCESS_TOKEN_EXPIRE_MINUTES = 15

    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def crypt(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    async def authenticate_user(self, user: User) -> Union[bool, User]:
        get_user_query = users_table.select().where(username=user.username)
        res = await db.fetch_one(get_user_query)

        if not user:
            return False
        if not self.verify_password(user.password, res.hashed_password):
            return False
        return res


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
                                        role_id=0
                                        )
    last_record_id = await db.execute(query)
    return {**user.dict(), "id": last_record_id}


@router.patch('/change_password', dependencies=[Depends(oauth2_scheme)])
async def change_password(user: ChangePass, token: str = Depends(oauth2_scheme)):
    pass


@router.patch('/change_car_model', dependencies=[Depends(oauth2_scheme)])
async def change_car_model(user: ChangeCarModel, token: str = Depends(oauth2_scheme)):
    pass


@router.post('/login')
async def login(user: User):
    user = await security.authenticate_user(user)
    if not user:
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
