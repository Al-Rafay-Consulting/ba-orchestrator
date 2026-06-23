"""
API Routes - Webhook endpoints for the BA Engine Orchestrator
"""

import json
import time
from datetime import datetime
from fastapi import APIRouter, HTTPException
from src.models.schemas import (
    SRSRequest, 
    APIResponse, 
    ErrorResponse,
    SRSResponse
)
from src.services.llm_service import LLMService
from src.services.validation_service import ValidationService
from src.utils.config import Config
from src.utils.logger import logger

router = APIRouter(prefix="/api", tags=["SRS Generation"])

# Initialize services
llm_service = LLMService()
validation_service = ValidationService()


@router.post("/generate-srs", response_model=APIResponse, status_code=200)
async def generate_srs(request: SRSRequest):
    """
    Main webhook endpoint for generating SRS from client request
    
    This endpoint:
    1. Receives unstructured client request
    2. Sends to Gemini AI for processing
    3. Validates the output
    4. Returns structured SRS JSON
    
    Args:
        request: SRSRequest containing client_request
        
    Returns:
        APIResponse with SRS data or error details
    """
    
    start_time = time.time()
    
    try:
        logger.info("=" * 60)
        logger.info("[INPUT] New SRS generation request received")
        logger.info(f"Client request length: {len(request.client_request)} chars")
        
        # Step 1: Send to LLM
        logger.info("Step 1/3: Sending to Gemini LLM for processing...")
        srs_dict = llm_service.generate_srs(request.client_request)
        
        if not srs_dict:
            logger.error("LLM returned no output")
            raise HTTPException(
                status_code=500,
                detail="Failed to generate SRS from LLM"
            )
        
        # Step 2: Validate and fix if needed
        logger.info("Step 2/3: Validating SRS structure...")
        is_valid, fixed_srs, error = validation_service.validate_and_fix(srs_dict)
        
        if not is_valid:
            logger.error(f"Validation failed: {error}")
            raise HTTPException(
                status_code=422,
                detail=f"Invalid SRS structure: {error}"
            )
        
        # Step 3: Save to file
        logger.info("Step 3/3: Saving results...")
        _save_srs_output(fixed_srs, request.client_request)
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        logger.info("[OK] SRS generation completed successfully")
        logger.info(f"Processing time: {processing_time:.2f}s")
        logger.info("=" * 60)
        
        # Build response
        return APIResponse(
            success=True,
            data=SRSResponse(**fixed_srs),
            metadata={
                "processing_time_ms": round(processing_time * 1000),
                "model": Config.GEMINI_MODEL,
                "timestamp": datetime.now().isoformat(),
                "validation_status": "passed"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Server error: {str(e)}"
        )


@router.get("/health", response_model=dict, status_code=200)
async def health_check():
    """Health check endpoint to verify service is running"""
    
    logger.info("Health check requested")
    
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "BA Engine Orchestrator",
        "version": "0.1.0"
    }


@router.post("/validate-srs", response_model=dict, status_code=200)
async def validate_srs(srs_data: dict):
    """
    Standalone endpoint to validate SRS JSON structure
    Useful for testing and debugging
    
    Args:
        srs_data: SRS dictionary to validate
        
    Returns:
        Validation results
    """
    
    logger.info("Validation request received")
    
    is_valid, error = validation_service.validate_srs(srs_data)
    
    return {
        "is_valid": is_valid,
        "error": error,
        "timestamp": datetime.now().isoformat()
    }


def _save_srs_output(srs_data: dict, client_request: str) -> None:
    """
    Save SRS output to a JSON file for record keeping
    
    Args:
        srs_data: The SRS data to save
        client_request: The original client request
    """
    
    try:
        import os
        os.makedirs("outputs", exist_ok=True)
        
        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"outputs/srs_{timestamp}.json"
        
        # Prepare data to save
        output = {
            "generated_at": datetime.now().isoformat(),
            "client_request": client_request,
            "srs": srs_data
        }
        
        # Write to file
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        logger.info(f"[OK] Output saved to {filename}")
        
    except Exception as e:
        logger.error(f"Failed to save output: {str(e)}")
