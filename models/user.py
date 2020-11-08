import sqlalchemy
from database import engine
from sqlalchemy.dialects.mysql import TEXT
from pydantic import BaseModel, Field
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
    username: Optional[str] = Field(
        None, title='Username', max_length=100,
    )
    password: Optional[str] = ''
    full_name: Optional[str] = Field(
        None, title='Full name', max_length=512
    )
    car_model: Optional[str] = Field(
        None, title='Car model', max_length=100
    )

    class Config:
        schema_extra = {
            'example': {
                'username': 'aleks0010v',
                'password': '123456',
                'full_name': 'Aleksandr V',
                'car_model': 'Maserati Ghibli III'
            }
        }


class UserInDB(BaseModel):
    username: str
    full_name: Optional[str] = ''
    hashed_password: str
    car_model: Optional[str] = ''
    role_id: int


class SecuredUserInfo(BaseModel):
    username: Optional[str] = Field(
        None, title='Username', max_length=100
    )
    full_name: Optional[str] = Field(
        None, title='Full name', max_length=512
    )
    car_model: Optional[str] = Field(
        None, title='Car model', max_length=100
    )

    class Config:
        schema_extra = {
            'example': {
                'username': 'aleks0010v',
                'full_name': 'Aleksandr V',
                'car_model': 'Maserati Ghibli III'
            }
        }


class Login(BaseModel):
    username: str
    password: str

    class Config:
        schema_extra = {
            'example': {
                'username': 'aleks0010v',
                'password': '123456'
            }
        }


class NewUser(BaseModel):
    username: str = Field(
        None, title='Username', max_length=100
    )
    password: str
    full_name: Optional[str] = Field(
        None, title='Full name', max_length=512
    )
    car_model: Optional[str] = Field(
        None, title='Car model', max_length=100
    )

    class Config:
        schema_extra = {
            'example': {
                'username': 'aleks0010v',
                'password': '123456',
                'full_name': 'Aleksandr V',
                'car_model': 'Maserati Ghibli III'
            }
        }


class NewUserResponse(BaseModel):
    id: int
    username: str
    full_name: str
    car_model: str

    class Config:
        schema_extra = {
            'example': {
                'username': 'aleks0010v',
                'id': 666,
                'full_name': 'Aleksandr V',
                'car_model': 'Maserati Ghibli III'
            }
        }


class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        schema_extra = {
            'example': {
                'access_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhbGVrcyIsImV4cCI6MTYwNDc3Mzg5Nn0.5DUFYCvxnpLcFzUbAnmZ7iRCflxXFzGQMQF6j-Bj0Xo',
                'token_type': 'bearer'
            }
        }

# ==================================================================================
