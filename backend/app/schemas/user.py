from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.models.user import UserRole

# Shared properties
class UserBase(BaseModel):
    email: EmailStr
    phone_number: str
    full_name: str
    role: UserRole = UserRole.CUSTOMER

# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str

# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    full_name: Optional[str] = None

class UserInDBBase(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Additional properties to return via API
class UserResponse(UserInDBBase):
    pass
