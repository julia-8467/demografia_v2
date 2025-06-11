from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from . import config
from .config import DATABASE_USERNAME

DATABASE_USERNAME= config.DATABASE_USERNAME
DATABASE_PASSWORD = config.DATABASE_PASSWORD
DATABASE_HOST = config.DATABASE_HOST
DATABASE_NAME = config.DATABASE_NAME

# Składamy connection string
SQLALCHEMY_DATABASE_URI = (
    f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}"
)

# Tworzenie silnika SQLAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)

# Tworzenie sesji
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Baza do deklarowania modeli
Base = declarative_base()

# Funkcja do pobierania sesji DB (przydatna w FastAPI np.)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
