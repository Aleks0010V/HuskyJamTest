from sqlalchemy import and_
from datetime import datetime

from database.schemas import schedule_table, users_table, tokens_table, roles_table


class Schedule:

    @staticmethod
    def get_all_unavailable_time_slots_query(master_id: int, date_time_obj: datetime):
        query = schedule_table.select().with_only_columns([schedule_table.c.date_time]) \
            .where(and_(schedule_table.c.master_id == master_id,
                        schedule_table.c.date_time.like(date_time_obj.date()
                                                        .strftime('%Y-%m-%d') + '%')))  # MySQL datetime format
        return query

    @staticmethod
    def get_user_time_slots(user_id: int, date_time_obj: datetime = None):
        if date_time_obj:
            query = schedule_table.select().with_only_columns([schedule_table.c.date_time]) \
                .where(and_(schedule_table.c.user_id == user_id,
                            schedule_table.c.date_time.like(date_time_obj.date()
                                                            .strftime('%Y-%m-%d') + '%')))  # MySQL datetime format
        else:
            query = schedule_table.select().with_only_columns([schedule_table.c.date_time])\
                .where(schedule_table.c.user_id == user_id)
        return query

    @staticmethod
    def create_an_appointment(**kwargs):
        return schedule_table.insert().values(**kwargs)


class User:

    @staticmethod
    def get_user_by_username(username: str):
        return users_table.select().where(users_table.c.username == username)

    @staticmethod
    def get_user_by_id(user_id: int):
        return users_table.select().where(users_table.c.id == user_id)

    @staticmethod
    def list_clients(date: str):
        return users_table\
            .select()\
            .with_only_columns([users_table.c.id, users_table.c.full_name])\
            .where(users_table.c.role_id == 0)

    @staticmethod
    def list_masters():
        return users_table\
            .select()\
            .with_only_columns([users_table.c.id, users_table.c.full_name])\
            .where(users_table.c.role_id == 1)

    @staticmethod
    def create_user(**kwargs):
        return users_table.insert().values(**kwargs)

    @staticmethod
    def get_master(master_id: int):
        return users_table.select().where(and_(users_table.c.id == master_id, users_table.c.role_id == 1))

    @staticmethod
    def check_name(name: str):
        return users_table.select().where(users_table.c.username == name)

    @staticmethod
    def update_user_info(username: str, **kwargs):
        return users_table.update().values(**kwargs).where(users_table.c.username == username)
