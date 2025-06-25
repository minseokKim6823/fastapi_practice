from datetime import datetime, timedelta, timezone
from sqlmodel import Field
from typing import Optional


KST = timezone(timedelta(hours=9))

def now_kst():
    return datetime.now(KST).replace(microsecond=0)


class TimestampMixin:
    created_at: Optional[datetime] = Field(default_factory=now_kst, nullable=False)
    updated_at: Optional[datetime] = Field(default_factory=now_kst, nullable=False)
