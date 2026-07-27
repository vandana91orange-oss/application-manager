from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings


print("ENV:", settings.ENV)
print("DATABASE_HOST:", repr(settings.DATABASE_HOST))
print("DATABASE_PORT:", settings.DATABASE_PORT)
print("DATABASE_NAME:", settings.DATABASE_NAME)
print("DATABASE_USER:", settings.DATABASE_USER)
# SQLAlchemy Engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=False,          # Set to True while debugging SQL queries
    pool_pre_ping=True,
)

# Session Factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Base Class
Base = declarative_base()


def get_db():
    """
    Dependency that provides a database session.
    """
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()