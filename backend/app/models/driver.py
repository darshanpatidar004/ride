from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.models.base import Base

class DriverStatus(str, enum.Enum):
    OFFLINE = "OFFLINE"
    ONLINE = "ONLINE"
    ON_TRIP = "ON_TRIP"
    SUSPENDED = "SUSPENDED"

class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    license_number = Column(String, unique=True, nullable=False)
    license_expiry = Column(DateTime, nullable=False)
    status = Column(Enum(DriverStatus), default=DriverStatus.OFFLINE)
    rating = Column(Float, default=0.0)
    total_trips = Column(Integer, default=0)
    is_approved = Column(Boolean, default=False)
    current_lat = Column(Float, nullable=True)
    current_lng = Column(Float, nullable=True)
    last_location_update = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="driver_profile")
    vehicles = relationship("Vehicle", back_populates="driver")
    trips = relationship("Booking", back_populates="driver", foreign_keys="[Booking.driver_id]")
