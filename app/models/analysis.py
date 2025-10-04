from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey
from .author import Base

class Analysis(Base):
    __tablename__ = 'analyses'

    id = Column(Integer, primary_key=True, index=True)
    analyze_date = Column(DateTime)
    average_commits = Column(Float)
    
    repository_id = Column(Integer, ForeignKey('repositories.id'))
    author_id = Column(Integer, ForeignKey('authors.id'))