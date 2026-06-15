from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.models.base import Base

class BookingStatus(str, enum.Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    ONGOING = "ONGOING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class BookingType(str, enum.Enum):
    INSTANT = "INSTANT"
    SCHEDULED = "SCHEDULED"
    HOURLY = "HOURLY"
    DAILY = "DAILY"

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=True)
    
    status = Column(Enum(BookingStatus), default=BookingStatus.PENDING, nullable=False)
    booking_type = Column(Enum(BookingType), default=BookingType.INSTANT, nullable=False)
    
    pickup_address = Column(String, nullable=False)
    pickup_lat = Column(Float, nullable=False)
    pickup_lng = Column(Float, nullable=False)
    
    dropoff_address = Column(String, nullable=False)
    dropoff_lat = Column(Float, nullable=False)
    dropoff_lng = Column(Float, nullable=False)
    
    scheduled_time = Column(DateTime(timezone=True), nullable=True)
    start_time = Column(DateTime(timezone=True), nullable=True)
    end_time = Column(DateTime(timezone=True), nullable=True)
    
    estimated_fare = Column(Float, nullable=False)
    actual_fare = Column(Float, nullable=True)
    distance_km = Column(Float, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    customer = relationship("User", back_populates="customer_bookings", foreign_keys=[customer_id])
    driver = relationship("Driver", back_populates="trips", foreign_keys=[driver_id])
    payment = relationship("Payment", back_populates="booking", uselist=False)
