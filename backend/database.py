from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# SQLite database file path
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./db/kalshi_council.db")

# Ensure the directory for the database exists
db_dir = os.path.dirname(DATABASE_URL.replace("sqlite:///./", "./"))
if db_dir and not os.path.exists(db_dir):
    os.makedirs(db_dir, exist_ok=True)

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_db():
    # Import models here to ensure they are registered with Base.metadata
    import backend.models
    Base.metadata.create_all(bind=engine)

# Auto-create tables on import
init_db()
