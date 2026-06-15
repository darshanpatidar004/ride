from pydantic import BaseModel
from app.models.payment import PaymentMethod, PaymentStatus

class PaymentBase(BaseModel):
    booking_id: int
    amount: float
    payment_method: PaymentMethod

class PaymentCreate(PaymentBase):
    pass

class PaymentResponse(PaymentBase):
    id: int
    status: PaymentStatus
    transaction_id: str | None = None
    
    class Config:
        from_attributes = True

class RazorpayOrderCreate(BaseModel):
    amount: float
    currency: str = "INR"
    receipt: str
