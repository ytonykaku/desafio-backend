from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.author import Base 

DATABASE_URL = "sqlite:///git_analysis_results.db"

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} 
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    from app.models import author, repository, analysis
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()