import sqlalchemy
from database import engine

metadata = sqlalchemy.MetaData(engine)


users_table = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("username", sqlalchemy.String(100), unique=True, index=True),
    sqlalchemy.Column("hashed_password", sqlalchemy.String(512)),
    sqlalchemy.Column("car_model", sqlalchemy.String(100)),
    sqlalchemy.Column("role_id", sqlalchemy.Integer),
)
if not engine.dialect.has_table(engine, users_table.name):
    metadata.create_all(tables=[users_table])

roles_table = sqlalchemy.Table(
    "roles",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("role", sqlalchemy.String(10), unique=True)
)
if not engine.dialect.has_table(engine, roles_table.name):
    metadata.create_all(tables=[roles_table])


tokens_table = sqlalchemy.Table(
    "tokens",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('token', sqlalchemy.Text, unique=True),
    sqlalchemy.Column("expires", sqlalchemy.DateTime()),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey("users.id")),
)
if not engine.dialect.has_table(engine, tokens_table.name):
    metadata.create_all(tables=[tokens_table])
