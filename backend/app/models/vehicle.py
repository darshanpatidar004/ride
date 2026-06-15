from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.base import Base

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=False)
    make = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    license_plate = Column(String, unique=True, nullable=False)
    color = Column(String, nullable=False)
    vehicle_type = Column(String, nullable=False) # e.g., Sedan, SUV, Hatchback
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    driver = relationship("Driver", back_populates="vehicles")
