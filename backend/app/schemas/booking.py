from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.booking import BookingStatus, BookingType

class BookingBase(BaseModel):
    pickup_address: str
    pickup_lat: float
    pickup_lng: float
    dropoff_address: str
    dropoff_lat: float
    dropoff_lng: float
    booking_type: BookingType = BookingType.INSTANT
    scheduled_time: Optional[datetime] = None

class BookingCreate(BookingBase):
    pass

class BookingUpdate(BaseModel):
    status: Optional[BookingStatus] = None
    driver_id: Optional[int] = None
    actual_fare: Optional[float] = None
    distance_km: Optional[float] = None

class BookingResponse(BookingBase):
    id: int
    customer_id: int
    driver_id: Optional[int] = None
    status: BookingStatus
    estimated_fare: float
    actual_fare: Optional[float] = None
    distance_km: Optional[float] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
