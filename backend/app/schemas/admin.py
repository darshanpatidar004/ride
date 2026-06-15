from pydantic import BaseModel
from typing import Optional
from app.models.user import UserRole
from app.models.driver import DriverStatus

class DriverAdminResponse(BaseModel):
    id: int
    user_id: int
    full_name: str
    email: str
    phone_number: str
    license_number: str
    status: DriverStatus
    is_approved: bool
    rating: float

    class Config:
        from_attributes = True

class UserAdminResponse(BaseModel):
    id: int
    full_name: str
    email: str
    phone_number: str
    role: UserRole
    is_active: bool

    class Config:
        from_attributes = True

class PricingRuleUpdate(BaseModel):
    base_fare: float
    per_km_charge: float
    gst_percentage: float
