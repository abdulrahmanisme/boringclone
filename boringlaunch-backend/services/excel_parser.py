from typing import List, Dict, Any
import pandas as pd
from pydantic import HttpUrl, ValidationError
from loguru import logger
from models import PlatformBase
from database import db

class ExcelParser:
    REQUIRED_COLUMNS = {
        "name": str,
        "url": str,
        "submission_type": str,
        "submission_endpoint": str,
        "api_key_required": bool
    }

    def __init__(self, file_path: str):
        self.file_path = file_path

    async def parse_platforms(self) -> List[PlatformBase]:
        """Parse platform data from Excel file"""
        try:
            # Read Excel file
            df = pd.read_excel(self.file_path)
            
            # Validate columns
            self._validate_columns(df)
            
            # Convert DataFrame to list of platforms
            platforms = []
            for _, row in df.iterrows():
                try:
                    platform = self._row_to_platform(row)
                    platforms.append(platform)
                except ValidationError as e:
                    logger.warning(f"Skipping invalid platform {row.get('name')}: {str(e)}")
                    continue
            
            return platforms

        except Exception as e:
            logger.error(f"Error parsing Excel file: {str(e)}")
            raise

    def _validate_columns(self, df: pd.DataFrame):
        """Validate that all required columns are present"""
        missing_columns = set(self.REQUIRED_COLUMNS.keys()) - set(df.columns)
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")

    def _row_to_platform(self, row: pd.Series) -> PlatformBase:
        """Convert DataFrame row to Platform model"""
        # Clean and prepare URL
        url = row["url"].strip()
        if not url.startswith(('http://', 'https://')):
            url = f"https://{url}"

        platform_data = {
            "name": row["name"].strip(),
            "url": HttpUrl(url),
            "submission_type": row["submission_type"].strip().lower(),
            "submission_endpoint": row["submission_endpoint"].strip() if pd.notna(row["submission_endpoint"]) else None,
            "api_key_required": bool(row["api_key_required"]) if pd.notna(row["api_key_required"]) else False,
            "is_active": True
        }
        
        # Validate submission type
        if platform_data["submission_type"] not in ["api", "selenium"]:
            raise ValueError(f"Invalid submission type for {platform_data['name']}: {platform_data['submission_type']}")
        
        # If submission type is API, endpoint is required
        if platform_data["submission_type"] == "api" and not platform_data["submission_endpoint"]:
            raise ValueError(f"API submission type requires endpoint for {platform_data['name']}")
        
        return PlatformBase(**platform_data)

    async def save_platforms(self) -> List[Dict[str, Any]]:
        """Parse and save platforms to database"""
        platforms = await self.parse_platforms()
        
        try:
            with db.transaction() as client:
                # Upsert platforms into database (update if exists, insert if not)
                result = client.table("platforms").upsert([
                    {
                        "name": p.name,
                        "url": str(p.url),
                        "submission_type": p.submission_type,
                        "submission_endpoint": p.submission_endpoint,
                        "api_key_required": p.api_key_required,
                        "is_active": p.is_active
                    }
                    for p in platforms
                ], on_conflict="name").execute()  # Use name as the conflict resolution column
                
                return result.data
                
        except Exception as e:
            logger.error(f"Error saving platforms to database: {str(e)}")
            raise