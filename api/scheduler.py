from fastapi import APIRouter, Depends
from pydantic import BaseModel

from auth import oauth2_scheme

router = APIRouter()


class Appointment(BaseModel):
    weekday: int  # 1-7
    time: int  # work hours


@router.post('/create_an_appointment')
async def create_an_appointment(time: Appointment, token: str = Depends(oauth2_scheme)):
    pass


@router.get('/')
def list_appointments(token: str = Depends(oauth2_scheme)):
    pass
