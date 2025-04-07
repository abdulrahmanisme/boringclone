from enum import Enum
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, HttpUrl, Field, validator

class SubmissionStatus(str, Enum):
    """Enum for submission statuses"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class SubmissionType(str, Enum):
    """Enum for submission types"""
    API = "api"
    SELENIUM = "selenium"

class StartupBase(BaseModel):
    """Base model for startup data"""
    name: str = Field(..., min_length=1, max_length=255, description="Company name")
    website: HttpUrl = Field(..., description="Company website URL")
    description: str = Field(..., min_length=10, description="Company description")
    tagline: Optional[str] = Field(None, max_length=200, description="Short company tagline")
    founded_year: Optional[int] = Field(None, ge=1900, le=datetime.now().year, description="Year the company was founded")
    logo_url: Optional[HttpUrl] = Field(None, description="URL to company logo")
    twitter_handle: Optional[str] = Field(None, pattern="^[A-Za-z0-9_]{1,15}$", description="Twitter handle without @")
    linkedin_url: Optional[HttpUrl] = Field(None, description="Company LinkedIn profile URL")

    @validator('website', 'linkedin_url', pre=True)
    def ensure_https(cls, v):
        """Ensure URLs use HTTPS"""
        if isinstance(v, str) and v.startswith('http://'):
            return v.replace('http://', 'https://')
        return v

class StartupCreate(StartupBase):
    """Model for creating a new startup"""
    pass

class Startup(StartupBase):
    """Model for startup with database fields"""
    id: int = Field(..., description="Unique startup ID")
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PlatformBase(BaseModel):
    """Base model for platform data"""
    name: str = Field(..., min_length=1, max_length=255, description="Platform name")
    url: HttpUrl = Field(..., description="Platform URL")
    submission_type: SubmissionType = Field(..., description="Type of submission process")
    submission_endpoint: Optional[str] = Field(None, description="API endpoint for submissions")
    api_key_required: bool = Field(False, description="Whether an API key is required")
    is_active: bool = Field(True, description="Whether the platform is active")

    @validator('submission_endpoint', always=True)
    def validate_endpoint(cls, v, values):
        """Validate that API submissions have an endpoint"""
        if values.get('submission_type') == SubmissionType.API and not v:
            raise ValueError("API submission type requires an endpoint")
        return v

class Platform(PlatformBase):
    """Model for platform with database fields"""
    id: int = Field(..., description="Unique platform ID")
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class SubmissionBase(BaseModel):
    """Base model for submission data"""
    startup_id: int = Field(..., gt=0, description="ID of the startup")
    platform_id: int = Field(..., gt=0, description="ID of the platform")
    status: SubmissionStatus = Field(default=SubmissionStatus.PENDING, description="Current submission status")
    error_message: Optional[str] = Field(None, description="Error message if submission failed")

class SubmissionCreate(SubmissionBase):
    """Model for creating a new submission"""
    pass

class Submission(SubmissionBase):
    """Model for submission with database fields and relationships"""
    id: int = Field(..., description="Unique submission ID")
    created_at: datetime
    updated_at: datetime
    startup: Optional[StartupBase] = Field(None, description="Related startup data")
    platform: Optional[PlatformBase] = Field(None, description="Related platform data")

    class Config:
        from_attributes = True
