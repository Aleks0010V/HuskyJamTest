from sqlalchemy import create_engine
from databases import Database

HOST = 'mysql://root:123456@localhost:3306/test_db'
engine = create_engine(HOST)
db = Database(HOST)
