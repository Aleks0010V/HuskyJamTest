import sqlalchemy
from database import engine
from sqlalchemy.dialects.mysql import TEXT
from pydantic import BaseModel
from typing import Optional

metadata = sqlalchemy.MetaData(engine)


users_table = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, unique=True),
    sqlalchemy.Column("username", sqlalchemy.String(100), unique=True, index=True),
    sqlalchemy.Column("full_name", sqlalchemy.String(512), default=''),
    sqlalchemy.Column("hashed_password", sqlalchemy.String(512)),
    sqlalchemy.Column("car_model", sqlalchemy.String(100), default=''),
    sqlalchemy.Column("role_id", sqlalchemy.ForeignKey('roles.id')),
)


roles_table = sqlalchemy.Table(
    "roles",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, unique=True, autoincrement=False),
    sqlalchemy.Column("role", sqlalchemy.String(10), unique=True)
)


tokens_table = sqlalchemy.Table(
    "tokens",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, unique=True),
    sqlalchemy.Column('token', TEXT),
    sqlalchemy.Column("expires", sqlalchemy.DateTime()),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey("users.id")),
)
metadata.create_all(tables=[roles_table, users_table, tokens_table], checkfirst=True)


# ==================================================================================
# ================================ models ==========================================
class UserInfo(BaseModel):
    username: Optional[str] = ''
    full_name: Optional[str] = ''
    password: Optional[str] = ''
    car_model: Optional[str] = ''


class UserInDB(BaseModel):
    username: Optional[str] = ''
    full_name: Optional[str] = ''
    hashed_password: Optional[str] = ''
    car_model: Optional[str] = ''


class SecuredUserInfo(BaseModel):
    username: Optional[str] = ''
    full_name: Optional[str] = ''
    hashed_password: Optional[str] = ''
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
