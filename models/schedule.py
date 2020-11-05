import sqlalchemy
from database import engine

from models import users_table

metadata = sqlalchemy.MetaData(engine)


schedule_table = sqlalchemy.Table(
    'schedule',
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, unique=True),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey(users_table.c.id)),
    sqlalchemy.Column("master_id", sqlalchemy.ForeignKey(users_table.c.id)),
    sqlalchemy.Column("date_time", sqlalchemy.DateTime)
)
if not engine.dialect.has_table(engine, schedule_table.name):
    if not engine.dialect.has_table(engine, users_table.name):
        metadata.create_all(tables=[users_table])
    metadata.create_all(tables=[schedule_table])
