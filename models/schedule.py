import sqlalchemy
from database import engine
from pydantic import BaseModel
from datetime import datetime

from models import users_table

metadata = sqlalchemy.MetaData(engine)


schedule_table = sqlalchemy.Table(
    'schedule',
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, unique=True, autoincrement=True),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey(users_table.c.id)),
    sqlalchemy.Column("master_id", sqlalchemy.ForeignKey(users_table.c.id)),
    sqlalchemy.Column("date_time", sqlalchemy.DateTime)
)
if not engine.dialect.has_table(engine, schedule_table.name):
    if not engine.dialect.has_table(engine, users_table.name):
        metadata.create_all(tables=[users_table])
    metadata.create_all(tables=[schedule_table])


# ==================================================================================
# ================================ models ==========================================
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


def get_all_unavailable_time_slots_query(master_id: int, date_time_obj: datetime):
    query = schedule_table.select().with_only_columns([schedule_table.c.date_time]) \
        .where(sqlalchemy.and_(schedule_table.c.master_id == master_id,
                               schedule_table.c.date_time.like(date_time_obj.date()
                                                               .strftime('%Y-%m-%d') + '%')))  # MySQL datetime format
    return query


def get_user_time_slots(user_id: int, date_time_obj: datetime = None):
    if date_time_obj:
        query = schedule_table.select().with_only_columns([schedule_table.c.date_time]) \
            .where(sqlalchemy.and_(schedule_table.c.user_id == user_id,
                                   schedule_table.c.date_time.like(date_time_obj.date()
                                                                   .strftime('%Y-%m-%d') + '%')))  # MySQL datetime format
    else:
        query = schedule_table.select().with_only_columns([schedule_table.c.date_time])\
            .where(schedule_table.c.user_id == user_id)
    return query
