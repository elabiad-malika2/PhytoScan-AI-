from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship 
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=False, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    role = Column(String, default="agriculteur")

    
    queries = relationship("Query", back_populates="user", cascade="all, delete-orphan")
    
    scans = relationship("PlantScan", back_populates="user", cascade="all, delete-orphan")
    
    # reports = relationship("Report", back_populates="user", cascade="all, delete-orphan")