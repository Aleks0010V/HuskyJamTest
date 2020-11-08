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
