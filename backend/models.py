from sqlalchemy import Column, Integer, String, Boolean, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from typing import Generator

# 🗃️ SQLite database config
DATABASE_URL = "sqlite:///./malnutrition_users.db"

# 🔌 SQLAlchemy Engine & Session factory
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# 📦 Declarative base for models
Base = declarative_base()

# 🔁 Dependency for injecting DB session in FastAPI routes
def get_db() -> Generator[Session, None, None]:
    """Yield a SQLAlchemy session and ensure proper cleanup."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 👤 User model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(256), nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(String(20), default="user")  # Can be: user, admin, doctor
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}', role='{self.role}')>"
