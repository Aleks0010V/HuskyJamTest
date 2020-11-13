from fastapi import APIRouter
from datetime import datetime
from typing import Optional

from auth import Security

from database.database import db, connect
from database.models import NewUser
from database.schemas import users_table
from database.crud import Schedule, User


# ==================================================================================
# ======================== configuration ===========================================
router = APIRouter()


@router.on_event("startup")
@connect
async def startup():  # create an admin on first start
    check_admin = users_table.select(users_table.c.id).where(users_table.c.role_id == 2)
    admin = await db.fetch_one(check_admin)
    if not admin:
        admin = {
            'username': 'admin',
            'hashed_password': Security.crypt('admin'),
            'role_id': 2
        }
        query = users_table.insert().values([admin])
        await db.execute(query)

# ==================================================================================


@router.get('/list_clients')
async def list_clients(date: Optional[str] = ''):
    """
    Returns a list of clients. Will be extended to return a list of clients for a specific day
    """
    query = User.list_clients(date)
    return await db.fetch_all(query)


@router.get('/client/{client_id}')
async def get_clients_schedule(client_id: int, date: Optional[str] = ''):
    """
    Returns a schedule of a specific client
    """
    if date:
        date_obj = datetime.strptime(date, "%d-%m-%Y")
    else:
        # this is done so because of get_user_time_slots implementation to return all ever created user`s appointments
        date_obj = None

    query = Schedule.get_user_time_slots(client_id, date_obj)
    return await db.fetch_all(query)


@router.get('/master/{master_id}')
async def get_masters_schedule(master_id: int, date: Optional[str] = ''):
    """
    Returns a schedule of a specific master
    """
    if date:
        date_obj = datetime.strptime(date, "%d-%m-%Y")
    else:
        date_obj = datetime.today()

    masters_hours = Schedule.get_all_unavailable_time_slots_query(master_id, date_obj)
    return await db.fetch_all(masters_hours)


@router.post('/create_master')
async def create_master(user: NewUser):
    query = User.create_user(username=user.username,
                               hashed_password=Security.crypt(user.password),
                               full_name=user.full_name,
                               role_id=1
                               )
    if not db.is_connected:
        await db.connect()
    last_record_id = await db.execute(query)
    res = {**user.dict(), "id": last_record_id}
    res.pop('password')
    return res
