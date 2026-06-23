"""
BA Engine Orchestrator - Main FastAPI Application
Convert messy client requests to structured SRS documents using AI
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import time

from src.utils.logger import logger
from src.utils.config import Config
from src.api.routes import router

# Create FastAPI application
app = FastAPI(
    title="BA Engine Orchestrator",
    description="Convert unstructured client requests to structured SRS documents using Google Gemini AI",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS (Cross-Origin Resource Sharing)
# Allows requests from different domains/ports
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Middleware to log requests and responses
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests"""
    
    # Log request
    logger.info(f"→ {request.method} {request.url.path}")
    
    start_time = time.time()
    
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        
        logger.info(f"← {response.status_code} ({process_time:.3f}s)")
        
        return response
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"✗ Error: {str(e)} ({process_time:.3f}s)")
        raise


# Include API routes
app.include_router(router)


# Root endpoint
@app.get("/", tags=["Info"])
async def root():
    """Root endpoint with API information"""
    return {
        "name": "BA Engine Orchestrator",
        "version": "0.1.0",
        "description": "Convert unstructured client requests to structured SRS documents",
        "endpoints": {
            "generate_srs": "POST /api/generate-srs",
            "health_check": "GET /api/health",
            "validate_srs": "POST /api/validate-srs",
            "documentation": "GET /docs"
        },
        "status": "running"
    }


# Startup event
@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    logger.info("\n" + "=" * 60)
    logger.info("[START] BA Engine Orchestrator Starting Up")
    logger.info("=" * 60)
    logger.info(f"API Host: {Config.API_HOST}:{Config.API_PORT}")
    logger.info(f"Debug Mode: {Config.API_DEBUG}")
    logger.info(f"Log Level: {Config.LOG_LEVEL}")
    logger.info(f"Gemini Model: {Config.GEMINI_MODEL}")
    logger.info("[OK] All systems ready")
    logger.info("=" * 60 + "\n")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    logger.info("\n" + "=" * 60)
    logger.info("[STOP] BA Engine Orchestrator Shutting Down")
    logger.info("=" * 60 + "\n")


# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle any unhandled exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "details": str(exc) if Config.API_DEBUG else "An error occurred"
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    # Run the application
    uvicorn.run(
        "src.main:app",
        host=Config.API_HOST,
        port=Config.API_PORT,
        reload=Config.API_DEBUG,
        log_level=Config.LOG_LEVEL.lower()
    )
