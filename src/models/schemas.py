"""
Pydantic models and schemas for request/response validation
"""

from typing import Optional, List
from pydantic import BaseModel, Field, validator


class SRSRequest(BaseModel):
    """Schema for incoming client request"""
    
    client_request: str = Field(
        ..., 
        min_length=10,
        max_length=5000,
        description="Unstructured client requirements text"
    )
    
    @validator('client_request')
    def client_request_not_empty(cls, v):
        """Ensure client request is not just whitespace"""
        if not v.strip():
            raise ValueError('Client request cannot be empty')
        return v.strip()
    
    class Config:
        json_schema_extra = {
            "example": {
                "client_request": "We need a system where customers can book appointments online, "
                                "get reminders, and the admin team can manage bookings."
            }
        }


class ProjectOverview(BaseModel):
    """Project overview section of SRS"""
    
    projectName: str
    clientDescription: str
    cleanDescription: str
    businessGoal: str


class FunctionalRequirement(BaseModel):
    """Individual functional requirement"""
    
    id: str
    title: str
    description: str
    priority: str = Field(..., pattern="^(CRITICAL|HIGH|MEDIUM|LOW)$")
    acceptance_criteria: List[str]


class NonFunctionalRequirement(BaseModel):
    """Individual non-functional requirement"""
    
    id: str
    title: str
    type: str  # e.g., Performance, Security, Scalability
    description: str


class Stakeholder(BaseModel):
    """Stakeholder information"""
    
    role: str
    description: str


class SRSResponse(BaseModel):
    """Schema for SRS output"""
    
    projectOverview: ProjectOverview
    objectives: List[str]
    stakeholders: List[Stakeholder]
    functionalRequirements: List[FunctionalRequirement]
    nonFunctionalRequirements: List[NonFunctionalRequirement]
    assumptions: List[str]
    constraints: Optional[List[str]] = []
    acceptanceCriteria: List[str]


class APIResponse(BaseModel):
    """Schema for API response wrapper"""
    
    success: bool
    data: Optional[SRSResponse] = None
    error: Optional[str] = None
    metadata: Optional[dict] = None


class ErrorResponse(BaseModel):
    """Error response schema"""
    
    success: bool = False
    error: str
    details: Optional[str] = None
