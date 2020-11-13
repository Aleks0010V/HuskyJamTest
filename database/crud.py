from sqlalchemy import and_
from datetime import datetime

from database.schemas import schedule_table


def get_all_unavailable_time_slots_query(master_id: int, date_time_obj: datetime):
    query = schedule_table.select().with_only_columns([schedule_table.c.date_time]) \
        .where(and_(schedule_table.c.master_id == master_id,
                    schedule_table.c.date_time.like(date_time_obj.date()
                                                    .strftime('%Y-%m-%d') + '%')))  # MySQL datetime format
    return query


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