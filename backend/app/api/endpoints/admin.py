from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.admin.admin_service import admin_service
from app.models.user import User, UserRole
from app.models.driver import Driver
from app.schemas.admin import DriverAdminResponse, UserAdminResponse, PricingRuleUpdate

router = APIRouter()

@router.get("/stats")
def get_stats(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized")
    return admin_service.get_dashboard_stats(db)

@router.get("/drivers", response_model=List[DriverAdminResponse])
def get_all_drivers(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    drivers = db.query(Driver).join(User).all()
    result = []
    for d in drivers:
        result.append({
            "id": d.id,
            "user_id": d.user_id,
            "full_name": d.user.full_name,
            "email": d.user.email,
            "phone_number": d.user.phone_number,
            "license_number": d.license_number,
            "status": d.status,
            "is_approved": d.is_approved,
            "rating": d.rating
        })
    return result

@router.post("/drivers/{driver_id}/approve")
def approve_driver(
    driver_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    driver = db.query(Driver).filter(Driver.id == driver_id).first()
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    
    driver.is_approved = True
    db.add(driver)
    db.commit()
    return {"message": "Driver approved successfully"}

@router.get("/users", response_model=List[UserAdminResponse])
def get_all_users(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized")
    return db.query(User).all()

@router.post("/users/{user_id}/toggle-active")
def toggle_user_active(
    user_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_active = not user.is_active
    db.add(user)
    db.commit()
    return {"message": f"User {'activated' if user.is_active else 'deactivated'} successfully"}

