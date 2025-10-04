from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session 
from app.models.author import Base 
from typing import Generator

DATABASE_URL = "sqlite:///git_analysis_results.db"

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} 
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db() -> None:
    from app.models import author, repository, analysis
    Base.metadata.create_all(bind=engine)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()