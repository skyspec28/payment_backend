from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Build the SQLAlchemy connection string from environment variables
SQLALCHEMY_DATABASE_URL = (
    f'postgresql://{settings.database_username}:{settings.database_password}'
    f'@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
)

# Create SQLAlchemy Engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Session Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
