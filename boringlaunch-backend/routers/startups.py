from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List, Optional
from loguru import logger
from models import Startup, StartupBase, StartupCreate
from database import db
from config import settings

router = APIRouter()

@router.post("/", response_model=Startup)
async def create_startup(startup: StartupCreate):
    """Create a new startup"""
    try:
        with db.transaction() as client:
            result = client.table("startups").insert({
                "name": startup.name,
                "website": str(startup.website),
                "description": startup.description,
                "tagline": startup.tagline,
                "founded_year": startup.founded_year,
                "logo_url": str(startup.logo_url) if startup.logo_url else None,
                "twitter_handle": startup.twitter_handle,
                "linkedin_url": str(startup.linkedin_url) if startup.linkedin_url else None
            }).execute()
            
            return Startup(**result.data[0])
    except Exception as e:
        logger.error(f"Error creating startup: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[Startup])
async def get_startups():
    """Get all startups"""
    try:
        with db.transaction() as client:
            result = client.table("startups").select("*").order("created_at", desc=True).execute()
            return [Startup(**item) for item in result.data]
    except Exception as e:
        logger.error(f"Error fetching startups: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{startup_id}", response_model=Startup)
async def get_startup(startup_id: int):
    """Get startup by ID"""
    try:
        with db.transaction() as client:
            result = client.table("startups").select("*").eq("id", startup_id).execute()
            if not result.data:
                raise HTTPException(status_code=404, detail="Startup not found")
            return Startup(**result.data[0])
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching startup {startup_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{startup_id}", response_model=Startup)
async def update_startup(startup_id: int, startup: StartupBase):
    """Update startup details"""
    try:
        with db.transaction() as client:
            # Check if startup exists
            existing = await get_startup(startup_id)
            
            # Update startup
            result = client.table("startups").update({
                "name": startup.name,
                "website": str(startup.website),
                "description": startup.description,
                "tagline": startup.tagline,
                "founded_year": startup.founded_year,
                "logo_url": str(startup.logo_url) if startup.logo_url else None,
                "twitter_handle": startup.twitter_handle,
                "linkedin_url": str(startup.linkedin_url) if startup.linkedin_url else None
            }).eq("id", startup_id).execute()
            
            return Startup(**result.data[0])
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating startup {startup_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{startup_id}")
async def delete_startup(startup_id: int):
    """Delete a startup"""
    try:
        with db.transaction() as client:
            # Check if startup exists
            existing = await get_startup(startup_id)
            
            # Delete startup
            result = client.table("startups").delete().eq("id", startup_id).execute()
            return {"message": "Startup deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting startup {startup_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{startup_id}/logo", response_model=Startup)
async def upload_logo(startup_id: int, file: UploadFile = File(...)):
    """Upload startup logo"""
    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")

    try:
        # Get existing startup
        existing = await get_startup(startup_id)
        
        # Upload file to Supabase storage
        with db.transaction() as client:
            storage = client.storage.from_("startup-logos")
            file_path = f"{startup_id}/{file.filename}"
            content = await file.read()
            
            # Upload file
            storage.upload(file_path, content)
            
            # Get public URL
            public_url = storage.get_public_url(file_path)
            
            # Update startup with new logo URL
            result = client.table("startups").update({
                "logo_url": public_url
            }).eq("id", startup_id).execute()
            
            return Startup(**result.data[0])
    except Exception as e:
        logger.error(f"Error uploading logo for startup {startup_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 