from sqlalchemy import Column, Integer, String, Date, Time, DateTime
from sqlalchemy.sql import func

from app.database.base import Base


class Calendar(Base):

    __tablename__ = "calendar_events"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    title = Column(
        String,
        nullable=False
    )


    date = Column(
        Date,
        nullable=True
    )


    time = Column(
        Time,
        nullable=True
    )


    location = Column(
        String,
        nullable=True
    )


    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )