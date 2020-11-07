from fastapi import APIRouter, Depends

from auth import Security
from models import UserInDB, Appointment, users_table
from database import db


# ==================================================================================
# ======================== configuration ===========================================
router = APIRouter()
security = Security(db)
# ==================================================================================


@router.post('/create_an_appointment')
async def create_an_appointment(info: Appointment, user: UserInDB = Depends(security.get_user_by_token)):
    pass


@router.get('/')
def list_appointments(user: UserInDB = Depends(security.get_user_by_token)):
    pass


@router.get('/list_masters')
async def list_masters(user: UserInDB = Depends(security.get_user_by_token)):
    """
    Returns a list of all masters.
    """
    query = users_table.select([users_table.c.full_name]).where(users_table.c.role_id == 1)
    return await db.fetch_all(query)


@router.get('/schedule/master/{master_id}')
async def get_masters_schedule(day, admin: UserInDB = Depends(security.get_user_by_token)):
    pass
