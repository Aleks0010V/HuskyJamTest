from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime
from sqlalchemy import and_

from auth import Security
from models import UserInDB, Appointment, users_table, schedule_table, get_all_unavailable_time_slots_query, get_user_time_slots
from database import db, connect


# ==================================================================================
# ======================== configuration ===========================================
router = APIRouter()


@router.on_event("startup")
@connect
async def startup():  # create a dummy master on first start
    check_master = users_table.select(users_table.c.id).where(users_table.c.role_id == 1)
    master = await db.fetch_one(check_master)
    if not master:
        master = {
            'username': 'master',
            'hashed_password': Security.crypt('master'),
            'full_name': 'dummy_master',
            'role_id': 1
        }
        query = users_table.insert().values([master])
        await db.execute(query)

# ==================================================================================


@router.post('/create_an_appointment')
async def create_an_appointment(info: Appointment, user: UserInDB = Depends(Security.get_user_by_token)):

    # validate date and time
    try:
        date_time_obj = datetime.strptime(info.date_time, '%d-%m-%Y %H:%M')
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid time",
            headers={"WWW-Authenticate": "Bearer"}
        )
    else:
        time_exception = HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                headers={"WWW-Authenticate": "Bearer"}
            )
        if date_time_obj.weekday() in [5, 6]:
            time_exception.detail = "Invalid time - weekend"
            raise time_exception
        if date_time_obj.time().hour < 10 or date_time_obj.time().hour > 20:
            time_exception.detail = "Invalid time - not a work hour (10 AM - 8 PM)"
            raise time_exception
        if date_time_obj.time().minute not in [0, 30]:  # set a session duration to be 30 minutes
            time_exception.detail = "Invalid time - minutes should be only 0 or 30"
            raise time_exception

        # fetch all unavailable slots
        query = get_all_unavailable_time_slots_query(info.master_id, date_time_obj)
        async for row in db.iterate(query):  # check if desired time is not in already booked time slots
            if date_time_obj == row[0]:
                time_exception.detail = "Time is not available"
                raise time_exception

    query = schedule_table.insert().values(user_id=user.id, master_id=info.master_id, date_time=date_time_obj)
    last_record_id = await db.execute(query)
    res = {**info.dict(), "id": last_record_id}
    return res


@router.get('/')
async def list_appointments(date: str = datetime.today().date().strftime("%d-%m-%Y"),
                            user: UserInDB = Depends(Security.get_user_by_token)):
    if date:
        date_obj = datetime.strptime(date, "%d-%m-%Y")
    else:
        date_obj = None

    query = get_user_time_slots(user.id, date_obj)
    return await db.fetch_all(query)


@router.get('/list_masters')
async def list_masters():
    """
    Returns a list of all masters.
    """
    query = users_table.select().with_only_columns([users_table.c.id, users_table.c.full_name]).where(users_table.c.role_id == 1)
    return await db.fetch_all(query)


@router.get('/master/{master_id}')
async def get_masters_schedule(master_id: int, date: str = datetime.today().date().strftime("%d-%m-%Y")):
    """
    Returns a master`s free hours for a specific day.
    """

    date_obj = datetime.strptime(date, "%d-%m-%Y")

    query = get_user_time_slots(master_id, date_obj)
    return await db.fetch_all(query)
