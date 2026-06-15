from sqlalchemy.orm import Session
from app.models.booking import Booking, BookingStatus
from app.models.driver import Driver, DriverStatus
from app.schemas.booking import BookingCreate, BookingUpdate
from fastapi import HTTPException, status
import math

class BookingService:
    @staticmethod
    def calculate_estimated_fare(pickup_lat, pickup_lng, dropoff_lat, dropoff_lng):
        # Dummy fare calculation: Base 50 + distance * 15
        # Haversine distance could be used for more accuracy
        distance = math.sqrt((pickup_lat - dropoff_lat)**2 + (pickup_lng - dropoff_lng)**2) * 111
        return round(50 + (distance * 15), 2)

    @staticmethod
    def create_booking(db: Session, customer_id: int, booking_in: BookingCreate):
        estimated_fare = BookingService.calculate_estimated_fare(
            booking_in.pickup_lat, booking_in.pickup_lng,
            booking_in.dropoff_lat, booking_in.dropoff_lng
        )
        
        db_booking = Booking(
            **booking_in.model_dump(),
            customer_id=customer_id,
            estimated_fare=estimated_fare,
            status=BookingStatus.PENDING
        )
        db.add(db_booking)
        db.commit()
        db.refresh(db_booking)
        return db_booking

    @staticmethod
    def find_nearby_drivers(db: Session, lat: float, lng: float, radius_km: float = 5.0):
        # Simplified proximity search
        # In production, use PostGIS for efficient geospatial queries
        drivers = db.query(Driver).filter(
            Driver.status == DriverStatus.ONLINE,
            Driver.is_approved == True
        ).all()
        
        nearby_drivers = []
        for d in drivers:
            if d.current_lat and d.current_lng:
                dist = math.sqrt((d.current_lat - lat)**2 + (d.current_lng - lng)**2) * 111
                if dist <= radius_km:
                    nearby_drivers.append(d)
        return nearby_drivers

    @staticmethod
    def update_booking_status(db: Session, booking_id: int, status_update: BookingStatus, driver_id: int = None):
        booking = db.query(Booking).filter(Booking.id == booking_id).first()
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")
        
        booking.status = status_update
        if driver_id:
            booking.driver_id = driver_id
            
        db.add(booking)
        db.commit()
        db.refresh(booking)
        return booking

booking_service = BookingService()
