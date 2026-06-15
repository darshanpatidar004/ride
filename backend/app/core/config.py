from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Ride Booking Platform"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DATABASE_URL: str
    
    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    
    # Redis
    REDIS_URL: str
    
    # Third Party APIs
    GOOGLE_MAPS_API_KEY: Optional[str] = None
    RAZORPAY_KEY_ID: Optional[str] = None
    RAZORPAY_KEY_SECRET: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
