from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.models.base import Base

class PaymentStatus(str, enum.Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"

class PaymentMethod(str, enum.Enum):
    CASH = "CASH"
    UPI = "UPI"
    RAZORPAY = "RAZORPAY"

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), unique=True, nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING, nullable=False)
    payment_method = Column(Enum(PaymentMethod), nullable=False)
    transaction_id = Column(String, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    booking = relationship("Booking", back_populates="payment")
