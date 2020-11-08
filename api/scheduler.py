from fastapi import APIRouter, Depends
from datetime import datetime

from auth import Security
from models import UserInDB, Appointment, users_table, schedule_table
from database import db, connect


# ==================================================================================
# ======================== configuration ===========================================
router = APIRouter()


@router.on_event("startup")
@connect
async def startup():
    pass

# ==================================================================================


@router.post('/create_an_appointment')
async def create_an_appointment(info: Appointment, user: UserInDB = Depends(Security.get_user_by_token)):
    pass


@router.get('/')
def list_appointments(user: UserInDB = Depends(Security.get_user_by_token)):
    pass


@router.get('/list_masters', dependencies=[Depends(Security.get_user_by_token)])
async def list_masters():
    """
    Returns a list of all masters.
    """
    query = users_table.select().with_only_columns([users_table.c.id, users_table.c.full_name]).where(users_table.c.role_id == 1)
    return await db.fetch_all(query)


@router.get('/master/{master_id}', dependencies=[Depends(Security.get_user_by_token)])
async def get_masters_schedule(master_id: int, date: str = datetime.today().date().strftime("%d-%m-%Y")):
    """
    Returns a master`s free hours for a specific day.
    """
    date_obj: datetime = datetime.strptime("%d-%m-%Y", date)  # convert string to datetime object to check everything

    query = schedule_table.select().with_only_columns().where()
    return await db.fetch_all(query)
