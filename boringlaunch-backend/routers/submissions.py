from fastapi import APIRouter, HTTPException
from typing import List
from loguru import logger
from models import Submission, SubmissionCreate, SubmissionStatus
from services.submission_service import SubmissionService
from database import db

router = APIRouter()
submission_service = SubmissionService()

@router.post("/", response_model=Submission)
async def create_submission(submission: SubmissionCreate):
    """Create a new submission"""
    try:
        # Validate that startup and platform exist
        startup = await submission_service.get_startup(submission.startup_id)
        if not startup:
            raise HTTPException(status_code=404, detail=f"Startup with ID {submission.startup_id} not found")
        
        platform = await submission_service.get_platform(submission.platform_id)
        if not platform:
            raise HTTPException(status_code=404, detail=f"Platform with ID {submission.platform_id} not found")
        
        # Create submission
        result = await submission_service.create_submission(submission)
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating submission: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[Submission])
async def get_submissions():
    """Get all submissions with startup and platform details"""
    try:
        with db.transaction() as client:
            result = client.table("submissions").select(
                "*",
                "startups:startup_id(*)",
                "platforms:platform_id(*)"
            ).execute()
            
            submissions = []
            for item in result.data:
                submission = Submission(
                    id=item["id"],
                    startup_id=item["startup_id"],
                    platform_id=item["platform_id"],
                    status=item["status"],
                    error_message=item["error_message"],
                    created_at=item["created_at"],
                    updated_at=item["updated_at"],
                    startup=item["startups"],
                    platform=item["platforms"]
                )
                submissions.append(submission)
            return submissions
    except Exception as e:
        logger.error(f"Error fetching submissions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{submission_id}", response_model=Submission)
async def get_submission(submission_id: int):
    """Get submission by ID with startup and platform details"""
    try:
        with db.transaction() as client:
            result = client.table("submissions").select(
                "*",
                "startups:startup_id(*)",
                "platforms:platform_id(*)"
            ).eq("id", submission_id).execute()
            
            if not result.data:
                raise HTTPException(status_code=404, detail="Submission not found")
            
            item = result.data[0]
            return Submission(
                id=item["id"],
                startup_id=item["startup_id"],
                platform_id=item["platform_id"],
                status=item["status"],
                error_message=item["error_message"],
                created_at=item["created_at"],
                updated_at=item["updated_at"],
                startup=item["startups"],
                platform=item["platforms"]
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching submission {submission_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/startup/{startup_id}", response_model=List[Submission])
async def get_submissions_by_startup(startup_id: int):
    """Get submissions for a specific startup with platform details"""
    try:
        # Check if startup exists
        startup = await submission_service.get_startup(startup_id)
        if not startup:
            raise HTTPException(status_code=404, detail=f"Startup with ID {startup_id} not found")
        
        with db.transaction() as client:
            result = client.table("submissions").select(
                "*",
                "startups:startup_id(*)",
                "platforms:platform_id(*)"
            ).eq("startup_id", startup_id).execute()
            
            submissions = []
            for item in result.data:
                submission = Submission(
                    id=item["id"],
                    startup_id=item["startup_id"],
                    platform_id=item["platform_id"],
                    status=item["status"],
                    error_message=item["error_message"],
                    created_at=item["created_at"],
                    updated_at=item["updated_at"],
                    startup=item["startups"],
                    platform=item["platforms"]
                )
                submissions.append(submission)
            return submissions
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching submissions for startup {startup_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{submission_id}/status", response_model=Submission)
async def update_status(submission_id: int, status: SubmissionStatus, error_message: str = None):
    """Update submission status"""
    try:
        # Check if submission exists
        submission = await submission_service.get_submission(submission_id)
        if not submission:
            raise HTTPException(status_code=404, detail="Submission not found")
        
        # Update status
        result = await submission_service.update_submission_status(
            submission_id=submission_id,
            status=status,
            error_message=error_message
        )
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating submission status for {submission_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 