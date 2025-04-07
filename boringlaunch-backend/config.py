from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Supabase settings
    SUPABASE_URL: str
    SUPABASE_KEY: str
    
    # Application settings
    APP_NAME: str = "BoringLaunch Clone"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"
    
    # CORS settings
    FRONTEND_URLS: list = ["http://localhost:5173", "http://localhost:5174", "http://localhost:5175"]
    
    # File upload settings
    MAX_UPLOAD_SIZE: int = 5 * 1024 * 1024  # 5MB
    ALLOWED_EXTENSIONS: set = {"xlsx", "xls"}
    
    # Selenium settings
    SELENIUM_TIMEOUT: int = 30
    SELENIUM_HEADLESS: bool = True
    
    # Redis settings (for future Celery integration)
    REDIS_URL: str = "redis://localhost:6379/0"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()

# Create a global settings instance
settings = get_settings() 