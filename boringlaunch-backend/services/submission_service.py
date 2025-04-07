from typing import Optional, List
from loguru import logger
from models import Submission, SubmissionCreate, Startup, Platform, SubmissionStatus
from database import db

class SubmissionService:
    async def create_submission(self, submission: SubmissionCreate) -> Submission:
        """Create a new submission record"""
        try:
            with db.transaction() as client:
                result = client.table("submissions").insert({
                    "startup_id": submission.startup_id,
                    "platform_id": submission.platform_id,
                    "status": submission.status,
                    "error_message": submission.error_message
                }).execute()
                
                return Submission(**result.data[0])
        except Exception as e:
            logger.error(f"Error creating submission: {str(e)}")
            raise

    async def get_submission(self, submission_id: int) -> Optional[Submission]:
        """Get submission by ID"""
        try:
            with db.transaction() as client:
                result = client.table("submissions").select("*").eq("id", submission_id).execute()
                if result.data:
                    return Submission(**result.data[0])
                return None
        except Exception as e:
            logger.error(f"Error fetching submission {submission_id}: {str(e)}")
            raise

    async def get_submissions_by_startup(self, startup_id: int) -> List[Submission]:
        """Get all submissions for a startup"""
        try:
            with db.transaction() as client:
                result = client.table("submissions").select("*").eq("startup_id", startup_id).execute()
                return [Submission(**item) for item in result.data]
        except Exception as e:
            logger.error(f"Error fetching submissions for startup {startup_id}: {str(e)}")
            raise

    async def update_submission_status(
        self, 
        submission_id: int, 
        status: SubmissionStatus, 
        error_message: Optional[str] = None
    ) -> Submission:
        """Update submission status and error message"""
        try:
            update_data = {"status": status}
            if error_message:
                update_data["error_message"] = error_message

            with db.transaction() as client:
                result = client.table("submissions").update(update_data).eq("id", submission_id).execute()
                return Submission(**result.data[0])
        except Exception as e:
            logger.error(f"Error updating submission {submission_id}: {str(e)}")
            raise

    async def get_startup(self, startup_id: int) -> Optional[Startup]:
        """Get startup details by ID"""
        try:
            with db.transaction() as client:
                result = client.table("startups").select("*").eq("id", startup_id).execute()
                if result.data:
                    return Startup(**result.data[0])
                return None
        except Exception as e:
            logger.error(f"Error fetching startup {startup_id}: {str(e)}")
            raise

    async def get_platform(self, platform_id: int) -> Optional[Platform]:
        """Get platform details by ID"""
        try:
            with db.transaction() as client:
                result = client.table("platforms").select("*").eq("id", platform_id).execute()
                if result.data:
                    return Platform(**result.data[0])
                return None
        except Exception as e:
            logger.error(f"Error fetching platform {platform_id}: {str(e)}")
            raise 