from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager
from loguru import logger
from config import settings
from routers import startups, platforms, submissions
from database import db

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    try:
        # Initialize database connection
        db.get_client()
        logger.info("Successfully connected to Supabase")
        yield
    finally:
        # Cleanup
        db.close()
        logger.info("Successfully cleaned up resources")

app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.FRONTEND_URLS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(startups.router, prefix=f"{settings.API_V1_PREFIX}/startups", tags=["startups"])
app.include_router(platforms.router, prefix=f"{settings.API_V1_PREFIX}/platforms", tags=["platforms"])
app.include_router(submissions.router, prefix=f"{settings.API_V1_PREFIX}/submissions", tags=["submissions"])

@app.get("/")
async def root():
    """Redirect root to API documentation"""
    return RedirectResponse(url="/docs")

@app.get("/health")
async def health_check():
    """Check application health"""
    is_healthy = await db.health_check()
    return {"status": "healthy" if is_healthy else "unhealthy"} 