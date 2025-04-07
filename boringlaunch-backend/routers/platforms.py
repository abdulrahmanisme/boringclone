from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import os
import tempfile
from loguru import logger
from models import Platform, PlatformBase
from services.excel_parser import ExcelParser
from database import db
from config import settings

router = APIRouter()

@router.post("/upload", response_model=List[Platform])
async def upload_platforms(
    file: UploadFile = File(...),
):
    """Upload Excel file with platform details"""
    # Validate file extension
    if not file.filename.endswith(tuple(settings.ALLOWED_EXTENSIONS)):
        raise HTTPException(
            status_code=400,
            detail=f"File must be one of: {settings.ALLOWED_EXTENSIONS}"
        )

    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name

        # Parse and save platforms
        parser = ExcelParser(temp_file_path)
        platforms = await parser.save_platforms()

        # Clean up temp file
        os.unlink(temp_file_path)

        return platforms

    except Exception as e:
        logger.error(f"Error processing platform upload: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[Platform])
async def get_platforms():
    """Get all platforms"""
    try:
        with db.transaction() as client:
            result = client.table("platforms").select("*").execute()
            return [Platform(**item) for item in result.data]
    except Exception as e:
        logger.error(f"Error fetching platforms: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{platform_id}", response_model=Platform)
async def get_platform(platform_id: int):
    """Get platform by ID"""
    try:
        with db.transaction() as client:
            result = client.table("platforms").select("*").eq("id", platform_id).execute()
            if not result.data:
                raise HTTPException(status_code=404, detail="Platform not found")
            return Platform(**result.data[0])
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching platform {platform_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{platform_id}/toggle", response_model=Platform)
async def toggle_platform(platform_id: int):
    """Toggle platform active status"""
    try:
        with db.transaction() as client:
            # Get current status
            platform = await get_platform(platform_id)
            
            # Toggle status
            result = client.table("platforms").update(
                {"is_active": not platform.is_active}
            ).eq("id", platform_id).execute()
            
            return Platform(**result.data[0])
    except Exception as e:
        logger.error(f"Error toggling platform {platform_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 