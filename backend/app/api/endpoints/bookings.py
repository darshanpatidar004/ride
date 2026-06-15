from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User
from app.schemas.booking import BookingCreate, BookingResponse
from app.services.booking_service import booking_service

router = APIRouter()

@router.post("/", response_model=BookingResponse)
def create_booking(
    *,
    db: Session = Depends(deps.get_db),
    booking_in: BookingCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create a new booking request.
    """
    return booking_service.create_booking(db=db, customer_id=current_user.id, booking_in=booking_in)

@router.get("/me", response_model=List[BookingResponse])
def read_my_bookings(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get all bookings for the current user.
    """
    return current_user.customer_bookings

@router.get("/{id}", response_model=BookingResponse)
def read_booking(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get booking by ID.
    """
    booking = db.query(deps.Booking).filter(deps.Booking.id == id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.customer_id != current_user.id and current_user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return booking
