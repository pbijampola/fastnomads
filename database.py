from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session,declarative_base

# SQLAlchemy setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./db.sqlite3"
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True, connect_args={"check_same_thread": False})

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the database tables
Base.metadata.create_all(bind=engine)