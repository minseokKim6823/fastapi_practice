from sqlalchemy import event
from sqlmodel import Field, SQLModel
from datetime import datetime, timedelta, timezone

KST = timezone(timedelta(hours=9))

def now_kst():
    return datetime.now(KST)


def register_timestamp_events():
    for cls in SQLModel.__subclasses__():
        if hasattr(cls, 'updated_at'):
            @event.listens_for(cls, "before_update", propagate=True)
            def receive_before_update(mapper, connection, target):
                target.updated_at = now_kst()
