from sqlalchemy.orm import Session
from app.models.repository import Repository

def get_by_url(db: Session, url: str) -> Repository | None:
    """Buscar um repositório pela URL"""
    return db.query(Repository).filter(Repository.url == url).first()

def create(db: Session, name: str, url: str) -> Repository:
    """Criar um novo repositório"""
    db_repo = Repository(name=name, url=url)
    db.add(db_repo)
    db.commit()
    db.refresh(db_repo)
    return db_repo