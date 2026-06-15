from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.models.base import Base

class UserRole(str, enum.Enum):
    CUSTOMER = "CUSTOMER"
    DRIVER = "DRIVER"
    ADMIN = "ADMIN"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    phone_number = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.CUSTOMER, nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    driver_profile = relationship("Driver", back_populates="user", uselist=False)
    customer_bookings = relationship("Booking", back_populates="customer", foreign_keys="[Booking.customer_id]")
