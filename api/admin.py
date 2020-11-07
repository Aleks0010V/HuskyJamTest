from fastapi import APIRouter, Depends

from auth import Security
from database import db
from models import users_table, UserInDB


# ==================================================================================
# ======================== configuration ===========================================
router = APIRouter()
security = Security(db)


@router.on_event("startup")
async def startup():
    await db.connect()
    check_admin = users_table.select([users_table.c.id]).where(users_table.c.role_id == 2)
    admin = await db.fetch_one(check_admin)
    if not admin:
        admin = {
            'username': 'admin',
            'password': 'admin',
            'role_id': 2
        }
        query = users_table.insert().values([admin])
        await db.execute(query)


@router.on_event("shutdown")
async def shutdown():
    await db.disconnect()

# ==================================================================================


@router.get('/list_clients')
async def list_clients(user: UserInDB = Depends(security.get_user_by_token)):
    query = users_table.select([users_table.c.full_name]).where(users_table.c.role_id == 0)
    return await db.fetch_all(query)


@router.get('/schedule/client/{client_id}')
async def get_clients_schedule(day, user: UserInDB = Depends(security.get_user_by_token)):
    pass
