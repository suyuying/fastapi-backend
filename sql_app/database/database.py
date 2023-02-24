# 其他系統這邊不用動
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..config import get_settings
# In this example, we are "connecting" to a SQLite database (opening a file with the SQLite database).
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

# db操作介面
engine = create_engine(
    get_settings().SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
# 建立session class ，當instance產生就可以透過engine跟db互動
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# 這個class是拿來之後繼承，並做表(create each of the database models or classes (the ORM models))
Base = declarative_base()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
