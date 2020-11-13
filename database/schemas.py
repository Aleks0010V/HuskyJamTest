import sqlalchemy
from database.database import engine
from sqlalchemy.dialects.mysql import TEXT

metadata = sqlalchemy.MetaData(engine)


roles_table = sqlalchemy.Table(
    "roles",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, unique=True, autoincrement=False),
    sqlalchemy.Column("role", sqlalchemy.String(10), unique=True)
)


users_table = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, unique=True, autoincrement=True),
    sqlalchemy.Column("username", sqlalchemy.String(100), unique=True, index=True),
    sqlalchemy.Column("full_name", sqlalchemy.String(512), default=''),
    sqlalchemy.Column("hashed_password", sqlalchemy.String(512)),
    sqlalchemy.Column("car_model", sqlalchemy.String(100), default=''),
    sqlalchemy.Column("role_id", sqlalchemy.ForeignKey(roles_table.c.id)),
)


tokens_table = sqlalchemy.Table(
    "tokens",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, unique=True, autoincrement=True),
    sqlalchemy.Column('token', TEXT),
    sqlalchemy.Column("expires", sqlalchemy.DateTime()),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey(users_table.c.id)),
)


schedule_table = sqlalchemy.Table(
    'schedule',
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, unique=True, autoincrement=True),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey(users_table.c.id)),
    sqlalchemy.Column("master_id", sqlalchemy.ForeignKey(users_table.c.id)),
    sqlalchemy.Column("date_time", sqlalchemy.DateTime)
)

metadata.create_all(tables=[roles_table, users_table, tokens_table, schedule_table], checkfirst=True)
