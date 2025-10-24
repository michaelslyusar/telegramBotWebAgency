"""
WWWizards Telegram Bot - Base Storage Service
"""
from abc import ABC, abstractmethod
from typing import List, Optional

from app.schemas.lead import LeadData, LeadResponse


class BaseStorageService(ABC):
    """Abstract base class for storage services."""
    
    @abstractmethod
    async def save_lead(self, lead_data: LeadData) -> LeadResponse:
        """Save lead data to storage."""
        pass
    
    @abstractmethod
    async def get_lead(self, lead_id: str) -> Optional[LeadData]:
        """Get lead data by ID."""
        pass
    
    @abstractmethod
    async def get_leads(self, limit: int = 100, offset: int = 0) -> List[LeadData]:
        """Get list of leads."""
        pass
    
    @abstractmethod
    async def update_lead_status(self, lead_id: str, status: str) -> bool:
        """Update lead status."""
        pass
    
    @abstractmethod
    async def delete_lead(self, lead_id: str) -> bool:
        """Delete lead."""
        pass


class StorageService:
    """Main storage service that delegates to appropriate implementation."""
    
    def __init__(self):
        """Initialize storage service."""
        from app.config import settings
        
        if settings.is_google_sheets_enabled():
            from app.services.storage_gsheets import GoogleSheetsStorageService
            self._storage = GoogleSheetsStorageService()
        else:
            from app.services.storage_sqlite import SQLiteStorageService
            self._storage = SQLiteStorageService()
    
    async def save_lead(self, lead_data: LeadData) -> LeadResponse:
        """Save lead data."""
        return await self._storage.save_lead(lead_data)
    
    async def get_lead(self, lead_id: str) -> Optional[LeadData]:
        """Get lead data by ID."""
        return await self._storage.get_lead(lead_id)
    
    async def get_leads(self, limit: int = 100, offset: int = 0) -> List[LeadData]:
        """Get list of leads."""
        return await self._storage.get_leads(limit, offset)
    
    async def update_lead_status(self, lead_id: str, status: str) -> bool:
        """Update lead status."""
        return await self._storage.update_lead_status(lead_id, status)
    
    async def delete_lead(self, lead_id: str) -> bool:
        """Delete lead."""
        return await self._storage.delete_lead(lead_id)

