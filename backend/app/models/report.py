# Modèle Report
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    scan_id = Column(Integer, ForeignKey("plant_scans.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    treatment_recommendation = Column(Text, nullable=False)
    
    pdf_path = Column(String, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    scan = relationship("PlantScan", back_populates="report")
    