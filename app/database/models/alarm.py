from sqlalchemy import Column, Integer, Time, String, Boolean, DateTime
from sqlalchemy.sql import func

from app.database.base import Base


class Alarm(Base):

    __tablename__ = "alarms"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    time = Column(
        Time,
        nullable=False
    )


    label = Column(
        String,
        nullable=True
    )


    enabled = Column(
        Boolean,
        default=True
    )


    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )