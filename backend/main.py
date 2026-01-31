"""
FastAPI application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from models import HealthResponse
from config import settings

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="Executable & Verifiable Governance for GenAI in Higher Education",
    version=settings.version,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version=settings.version,
        timestamp=datetime.now()
    )


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "app": settings.app_name,
        "version": settings.version,
        "environment": settings.environment,
        "docs": "/docs",
        "api_docs": "/redoc"
    }


# Routers
try:
    from governance_middleware.api import router as governance_router
    app.include_router(governance_router, tags=["Governance"])
except Exception:
    # In case module not ready; app still serves health
    pass


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.backend_host,
        port=settings.backend_port,
        reload=settings.debug
    )
