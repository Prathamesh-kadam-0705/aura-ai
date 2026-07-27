from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from app.database.base import Base


class Memory(Base):
    __tablename__ = "memories"

    id = Column(Integer, primary_key=True, index=True)

    category = Column(String, nullable=False)

    key = Column(String, nullable=False, index=True)

    value = Column(String, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())