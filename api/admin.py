from fastapi import APIRouter, Depends
from datetime import datetime

from auth import Security, check_admin_role
from database import db, connect
from models import users_table, UserInDB


# ==================================================================================
# ======================== configuration ===========================================
router = APIRouter()


@router.on_event("startup")
@connect
async def startup():
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


@router.get('/list_clients', dependencies=[Depends(check_admin_role)])
async def list_clients():
    query = users_table.select().with_only_columns([users_table.c.id, users_table.c.full_name]).where(users_table.c.role_id == 0)
    return await db.fetch_all(query)


@router.get('/client/{client_id}', dependencies=[Depends(check_admin_role)])
async def get_clients_schedule(client_id: int, date: str = datetime.today().date().strftime("%d-%m-%Y")):
    date_obj: datetime = datetime.strptime("%d-%m-%Y", date)  # convert string to datetime object to check everything
