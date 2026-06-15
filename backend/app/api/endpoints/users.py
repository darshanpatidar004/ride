from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate

router = APIRouter()

@router.get("/me", response_model=UserResponse)
def read_user_me(
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user

@router.put("/me", response_model=UserResponse)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    update_data = user_in.model_dump(exclude_unset=True)
    if update_data.get("password"):
        from app.auth.security import get_password_hash
        hashed_password = get_password_hash(update_data["password"])
        del update_data["password"]
        update_data["hashed_password"] = hashed_password
        
    for field in update_data:
        setattr(current_user, field, update_data[field])
        
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user
