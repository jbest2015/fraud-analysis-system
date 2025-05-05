from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from typing import Optional
from pathlib import Path

from ..models.database_models import Base

class DatabaseManager:
    def __init__(self, db_path: str = "data/fraud_database.sqlite"):
        # Ensure the data directory exists
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Create database engine
        self.engine = create_engine(f"sqlite:///{db_path}", echo=True)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
    def init_db(self):
        """Initialize the database schema"""
        Base.metadata.create_all(bind=self.engine)
        
    def get_session(self) -> Session:
        """Get a new database session"""
        return self.SessionLocal()
    
    def close(self):
        """Close the database connection"""
        self.engine.dispose()