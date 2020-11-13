from sqlalchemy.dialects.mysql import TEXT
from pydantic import BaseModel, Field
from typing import Optional


# ================================== user ==========================================
# ==================================================================================
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
    id: int
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


# ================================== appointment ===================================
# ==================================================================================
class Appointment(BaseModel):
    master_id: int
    date_time: str

    class Config:
        schema_extra = {
            'example': {
                'master_id': 12345,
                'date_time': '15-11-2020 14:00'
            }
        }
