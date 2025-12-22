from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from chalicelib.config import get_db_url


engine = create_engine(
    get_db_url(),
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
