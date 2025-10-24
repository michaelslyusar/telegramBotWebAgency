"""
WWWizards Telegram Bot - Lead Data Schema
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class LeadData(BaseModel):
    """Lead data model for order quiz."""
    
    # User information
    user_id: int = Field(..., description="Telegram user ID")
    username: Optional[str] = Field(None, description="Telegram username")
    first_name: Optional[str] = Field(None, description="User first name")
    last_name: Optional[str] = Field(None, description="User last name")
    
    # Project information
    service_type: str = Field(..., description="Type of service requested")
    budget: str = Field(..., description="Project budget range")
    timeline: str = Field(..., description="Project timeline")
    
    # Contact information
    company_name: str = Field(..., description="Company name")
    contact_name: str = Field(..., description="Contact person name")
    contact_phone: str = Field(..., description="Contact phone number")
    contact_email: str = Field(..., description="Contact email")
    
    # Additional information
    additional_info: str = Field("", description="Additional project information")
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.now, description="Lead creation timestamp")
    status: str = Field("new", description="Lead status")
    
    class Config:
        """Pydantic config."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class LeadResponse(BaseModel):
    """Response model for lead operations."""
    
    success: bool = Field(..., description="Operation success status")
    message: str = Field(..., description="Response message")
    lead_id: Optional[str] = Field(None, description="Lead ID if created")
    
    class Config:
        """Pydantic config."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

