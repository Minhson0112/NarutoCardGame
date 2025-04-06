from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager
from bot.config.config import DB_CONFIG

Base = declarative_base()

dbUrl = f"mysql+mysqlconnector://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['database']}"
engine = create_engine(dbUrl, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def getDbSession():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
