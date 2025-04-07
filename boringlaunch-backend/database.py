from typing import Optional
from supabase import create_client, Client
from contextlib import contextmanager
from loguru import logger
from config import settings

class Database:
    _instance: Optional[Client] = None
    
    @classmethod
    def get_client(cls) -> Client:
        """Get or create Supabase client instance"""
        if cls._instance is None:
            try:
                cls._instance = create_client(
                    settings.SUPABASE_URL,
                    settings.SUPABASE_KEY
                )
                logger.info("Successfully connected to Supabase")
            except Exception as e:
                logger.error(f"Failed to connect to Supabase: {str(e)}")
                raise
        return cls._instance

    @classmethod
    @contextmanager
    def transaction(cls):
        """Context manager for database transactions"""
        client = cls.get_client()
        try:
            yield client
            # Note: Supabase-py doesn't support explicit transactions yet
            # This is a placeholder for future implementation
        except Exception as e:
            logger.error(f"Database transaction failed: {str(e)}")
            raise
    
    @classmethod
    async def health_check(cls) -> bool:
        """Check if database connection is healthy"""
        try:
            client = cls.get_client()
            # Simple query to check connection
            result = client.table("platforms").select("count", count="exact").execute()
            return True
        except Exception as e:
            logger.error(f"Database health check failed: {str(e)}")
            return False

    @classmethod
    def close(cls):
        """Close database connection"""
        if cls._instance is not None:
            # Note: Supabase-py doesn't have explicit close method
            # This is a placeholder for cleanup
            cls._instance = None
            logger.info("Database connection closed")

# Create global database instance
db = Database() 