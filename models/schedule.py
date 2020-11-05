import sqlalchemy
from database import engine

metadata = sqlalchemy.MetaData(engine)


schedule_table = sqlalchemy.Table(
    'schedule',
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.Integer),
    sqlalchemy.Column("master_id", sqlalchemy.Integer),
    sqlalchemy.Column("date_time", sqlalchemy.DateTime)
)
if not engine.dialect.has_table(engine, schedule_table.name):
    metadata.create_all(tables=[schedule_table])
