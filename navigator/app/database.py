from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

# --- Use absolute path for the database ---
# Get the absolute path to the directory where this file is located
_current_dir = os.path.dirname(os.path.abspath(__file__))
# Go up one level to the 'navigator' directory
_navigator_dir = os.path.dirname(_current_dir)
DATABASE_URL = f"sqlite:///{os.path.join(_navigator_dir, 'navigator.db')}"


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    # create_all already checks for table existence, so this is robust.
    Base.metadata.create_all(bind=engine)

# --- Dependency for API endpoints ---
def get_db():
    """
    FastAPI dependency that provides a database session for each request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
