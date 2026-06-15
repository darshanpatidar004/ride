from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.booking import Booking, BookingStatus
from app.models.payment import Payment, PaymentStatus
from app.models.user import User

class AdminService:
    @staticmethod
    def get_dashboard_stats(db: Session):
        total_revenue = db.query(func.sum(Payment.amount)).filter(Payment.status == PaymentStatus.COMPLETED).scalar() or 0
        active_trips = db.query(func.count(Booking.id)).filter(Booking.status.in_([BookingStatus.ACCEPTED, BookingStatus.ONGOING])).scalar()
        total_customers = db.query(func.count(User.id)).filter(User.role == "CUSTOMER").scalar()
        total_drivers = db.query(func.count(User.id)).filter(User.role == "DRIVER").scalar()
        
        return {
            "total_revenue": float(total_revenue),
            "active_trips": active_trips,
            "total_customers": total_customers,
            "total_drivers": total_drivers
        }

admin_service = AdminService()
