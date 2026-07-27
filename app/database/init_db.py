from app.database.base import Base
from app.database.connection import engine

import database.models


def init_database():
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created.")


if __name__ == "__main__":
    init_database()