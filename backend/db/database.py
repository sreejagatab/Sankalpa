from contextlib import contextmanager
import sys
import os
from typing import Generator, Optional, Dict, Any

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from core.config import config
from core.logging import get_logger

logger = get_logger("database")

# Base class for ORM models
Base = declarative_base()

# Naming convention for constraints
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

class Database:
    """Database connection manager with connection pooling"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize the database connection"""
        # Get database URL from configuration
        storage_type = config.get("memory.default_store")
        
        if storage_type == "postgres":
            db_url = config.get("memory.postgres_url")
            if not db_url:
                # Build connection URL from components
                user = config.get("postgres.user", "postgres")
                password = config.get("postgres.password", "postgres")
                host = config.get("postgres.host", "localhost")
                port = config.get("postgres.port", "5432")
                db = config.get("postgres.db", "sankalpa")
                
                db_url = f"postgresql://{user}:{password}@{host}:{port}/{db}"
                
            # Create engine with connection pooling
            self.engine = create_engine(
                db_url,
                pool_size=10,
                max_overflow=20,
                pool_recycle=3600,  # Recycle connections after 1 hour
                pool_pre_ping=True  # Check connection liveliness
            )
            
            # Create session factory
            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )
            
            self.available = True
            logger.info(f"PostgreSQL database initialized: {db_url}")
            
        else:
            # No database configured
            self.engine = None
            self.SessionLocal = None
            self.available = False
            logger.warning("No database configured, some features may be limited")
    
    def create_tables(self):
        """Create all database tables"""
        if not self.available:
            logger.warning("Cannot create tables: database not available")
            return
            
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info("Database tables created")
        except Exception as e:
            logger.error(f"Failed to create database tables: {str(e)}")
    
    def get_session(self) -> Optional[Session]:
        """Get a new database session
        
        Returns:
            SQLAlchemy session or None if database not available
        """
        if not self.available:
            return None
            
        return self.SessionLocal()
    
    @contextmanager
    def session_scope(self) -> Generator[Session, None, None]:
        """Session context manager with automatic commit/rollback
        
        Yields:
            SQLAlchemy session
            
        Raises:
            Exception: If database is not available
        """
        if not self.available:
            raise Exception("Database not available")
            
        session = self.get_session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
    
    def execute(self, query: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """Execute a raw SQL query
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            Query result
            
        Raises:
            Exception: If database is not available
        """
        if not self.available:
            raise Exception("Database not available")
            
        with self.engine.connect() as connection:
            result = connection.execute(query, params or {})
            return result

# Global database instance
db = Database()

# Dependency for FastAPI routes
def get_db():
    """Get a database session for use in FastAPI routes"""
    if not db.available:
        raise Exception("Database not available")
        
    session = db.get_session()
    try:
        yield session
    finally:
        session.close()