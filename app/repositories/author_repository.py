from sqlalchemy.orm import Session
from app.models.author import Author

def get_by_name(db: Session, name: str) -> Author | None:
    """Buscar um autor pelo nome"""
    return db.query(Author).filter(Author.name == name).first()

def create(db: Session, name: str) -> Author:
    """Criar um novo autor"""
    db_author = Author(name=name)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author