from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional

from auth import oauth2_scheme

router = APIRouter()


class User(BaseModel):
    username: str
    password: Optional[str] = ''
    car_model: Optional[str] = ''


@router.post('/create_user')
async def create_user(user: User):
    pass


@router.patch('/change_password', dependencies=[Depends(oauth2_scheme)])
async def change_password(user: User, token: str = Depends(oauth2_scheme)):
    pass


@router.patch('/change_car_model', dependencies=[Depends(oauth2_scheme)])
async def change_car_model(user: User, token: str = Depends(oauth2_scheme)):
    pass


@router.post('/login')
def login(user: User):
    pass
