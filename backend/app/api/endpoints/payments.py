from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.services.payment_service import payment_service
from app.models.payment import Payment, PaymentStatus
from app.schemas.payment import PaymentCreate, PaymentResponse

router = APIRouter()

@router.post("/create-order")
def create_order(
    *,
    db: Session = Depends(deps.get_db),
    amount: float,
    booking_id: int,
    current_user: deps.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create a Razorpay order for a booking.
    """
    # Verify booking belongs to user
    booking = db.query(deps.Booking).filter(deps.Booking.id == booking_id).first()
    if not booking or booking.customer_id != current_user.id:
        raise HTTPException(status_code=404, detail="Booking not found")

    order = payment_service.create_razorpay_order(
        amount_in_paise=int(amount * 100),
        receipt=f"receipt_booking_{booking_id}"
    )
    return order

@router.post("/verify", response_model=PaymentResponse)
def verify_payment(
    *,
    db: Session = Depends(deps.get_db),
    razorpay_order_id: str,
    razorpay_payment_id: str,
    razorpay_signature: str,
    booking_id: int,
) -> Any:
    """
    Verify Razorpay payment and update booking/payment status.
    """
    params_dict = {
        'razorpay_order_id': razorpay_order_id,
        'razorpay_payment_id': razorpay_payment_id,
        'razorpay_signature': razorpay_signature
    }
    
    if not payment_service.verify_payment_signature(params_dict):
        raise HTTPException(status_code=400, detail="Invalid payment signature")
    
    # Update or create payment record
    payment = db.query(Payment).filter(Payment.booking_id == booking_id).first()
    if not payment:
        # Should normally exist if order was created, but handling for safety
        booking = db.query(deps.Booking).filter(deps.Booking.id == booking_id).first()
        payment = Payment(
            booking_id=booking_id,
            amount=booking.estimated_fare,
            payment_method="RAZORPAY",
            status=PaymentStatus.COMPLETED,
            transaction_id=razorpay_payment_id
        )
        db.add(payment)
    else:
        payment.status = PaymentStatus.COMPLETED
        payment.transaction_id = razorpay_payment_id
        
    db.commit()
    db.refresh(payment)
    return payment
