"""
WWWizards Telegram Bot - SQLite Storage Service
"""
import aiosqlite
from datetime import datetime
from typing import List, Optional
from pathlib import Path

from loguru import logger

from app.config import settings
from app.logging_config import log_storage_operation
from app.schemas.lead import LeadData, LeadResponse


class SQLiteStorageService:
    """SQLite storage service implementation."""
    
    def __init__(self):
        """Initialize SQLite service."""
        self.db_path = settings.data_dir / "bot.db"
        self.db_path.parent.mkdir(exist_ok=True)
    
    async def _get_connection(self) -> aiosqlite.Connection:
        """Get database connection."""
        return await aiosqlite.connect(self.db_path)
    
    async def save_lead(self, lead_data: LeadData) -> LeadResponse:
        """Save lead data to SQLite."""
        try:
            async with await self._get_connection() as conn:
                cursor = await conn.execute("""
                    INSERT INTO leads (
                        user_id, username, first_name, last_name,
                        service_type, budget, timeline, company_name,
                        contact_name, contact_phone, contact_email,
                        additional_info, status, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    lead_data.user_id,
                    lead_data.username,
                    lead_data.first_name,
                    lead_data.last_name,
                    lead_data.service_type,
                    lead_data.budget,
                    lead_data.timeline,
                    lead_data.company_name,
                    lead_data.contact_name,
                    lead_data.contact_phone,
                    lead_data.contact_email,
                    lead_data.additional_info,
                    lead_data.status,
                    lead_data.created_at.isoformat()
                ))
                
                lead_id = str(cursor.lastrowid)
                await conn.commit()
                
                log_storage_operation("save_lead", True, lead_id=lead_id)
                logger.info(f"Lead saved to SQLite: {lead_id}")
                
                return LeadResponse(
                    success=True,
                    message="Lead saved successfully",
                    lead_id=lead_id
                )
                
        except Exception as e:
            log_storage_operation("save_lead", False, error=str(e))
            logger.error(f"Error saving lead to SQLite: {e}")
            return LeadResponse(
                success=False,
                message=f"Failed to save lead: {e}"
            )
    
    async def get_lead(self, lead_id: str) -> Optional[LeadData]:
        """Get lead data by ID."""
        try:
            async with await self._get_connection() as conn:
                cursor = await conn.execute("""
                    SELECT * FROM leads WHERE id = ?
                """, (lead_id,))
                
                row = await cursor.fetchone()
                if not row:
                    return None
                
                lead_data = LeadData(
                    user_id=row[1],
                    username=row[2],
                    first_name=row[3],
                    last_name=row[4],
                    service_type=row[5],
                    budget=row[6],
                    timeline=row[7],
                    company_name=row[8],
                    contact_name=row[9],
                    contact_phone=row[10],
                    contact_email=row[11],
                    additional_info=row[12],
                    status=row[13],
                    created_at=datetime.fromisoformat(row[14])
                )
                
                log_storage_operation("get_lead", True, lead_id=lead_id)
                return lead_data
                
        except Exception as e:
            log_storage_operation("get_lead", False, error=str(e), lead_id=lead_id)
            logger.error(f"Error getting lead from SQLite: {e}")
            return None
    
    async def get_leads(self, limit: int = 100, offset: int = 0) -> List[LeadData]:
        """Get list of leads."""
        try:
            async with await self._get_connection() as conn:
                cursor = await conn.execute("""
                    SELECT * FROM leads 
                    ORDER BY created_at DESC 
                    LIMIT ? OFFSET ?
                """, (limit, offset))
                
                rows = await cursor.fetchall()
                leads = []
                
                for row in rows:
                    lead_data = LeadData(
                        user_id=row[1],
                        username=row[2],
                        first_name=row[3],
                        last_name=row[4],
                        service_type=row[5],
                        budget=row[6],
                        timeline=row[7],
                        company_name=row[8],
                        contact_name=row[9],
                        contact_phone=row[10],
                        contact_email=row[11],
                        additional_info=row[12],
                        status=row[13],
                        created_at=datetime.fromisoformat(row[14])
                    )
                    leads.append(lead_data)
                
                log_storage_operation("get_leads", True, count=len(leads))
                return leads
                
        except Exception as e:
            log_storage_operation("get_leads", False, error=str(e))
            logger.error(f"Error getting leads from SQLite: {e}")
            return []
    
    async def update_lead_status(self, lead_id: str, status: str) -> bool:
        """Update lead status."""
        try:
            async with await self._get_connection() as conn:
                await conn.execute("""
                    UPDATE leads SET status = ? WHERE id = ?
                """, (status, lead_id))
                
                await conn.commit()
                
                log_storage_operation("update_lead_status", True, lead_id=lead_id, status=status)
                return True
                
        except Exception as e:
            log_storage_operation("update_lead_status", False, error=str(e), lead_id=lead_id)
            logger.error(f"Error updating lead status in SQLite: {e}")
            return False
    
    async def delete_lead(self, lead_id: str) -> bool:
        """Delete lead."""
        try:
            async with await self._get_connection() as conn:
                await conn.execute("""
                    DELETE FROM leads WHERE id = ?
                """, (lead_id,))
                
                await conn.commit()
                
                log_storage_operation("delete_lead", True, lead_id=lead_id)
                return True
                
        except Exception as e:
            log_storage_operation("delete_lead", False, error=str(e), lead_id=lead_id)
            logger.error(f"Error deleting lead from SQLite: {e}")
            return False

