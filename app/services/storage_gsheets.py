"""
WWWizards Telegram Bot - Google Sheets Storage Service
"""
import json
from datetime import datetime
from typing import List, Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from loguru import logger

from app.config import settings
from app.logging_config import log_storage_operation
from app.schemas.lead import LeadData, LeadResponse


class GoogleSheetsStorageService:
    """Google Sheets storage service implementation."""
    
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    
    def __init__(self):
        """Initialize Google Sheets service."""
        self.service = None
        self.spreadsheet_id = settings.GOOGLE_SHEETS_SPREADSHEET_ID
        self.worksheet_name = settings.GOOGLE_SHEETS_WORKSHEET_NAME
        self._initialize_service()
    
    def _initialize_service(self) -> None:
        """Initialize Google Sheets API service."""
        try:
            creds = None
            creds_file = settings.google_credentials_path
            
            if not creds_file or not creds_file.exists():
                raise FileNotFoundError(f"Credentials file not found: {creds_file}")
            
            # Load credentials
            with open(creds_file, 'r') as token:
                creds_data = json.load(token)
            
            # Create credentials object
            creds = Credentials.from_authorized_user_info(creds_data, self.SCOPES)
            
            # Build service
            self.service = build('sheets', 'v4', credentials=creds)
            
            log_storage_operation("google_sheets_init", True)
            logger.info("Google Sheets service initialized successfully")
            
        except Exception as e:
            log_storage_operation("google_sheets_init", False, error=str(e))
            logger.error(f"Failed to initialize Google Sheets service: {e}")
            raise
    
    async def save_lead(self, lead_data: LeadData) -> LeadResponse:
        """Save lead data to Google Sheets."""
        try:
            # Prepare row data
            row_data = [
                datetime.now().isoformat(),  # Timestamp
                str(lead_data.user_id),      # User ID
                lead_data.username or "",    # Username
                lead_data.first_name or "",  # First name
                lead_data.last_name or "",   # Last name
                lead_data.service_type,      # Service type
                lead_data.budget,            # Budget
                lead_data.timeline,          # Timeline
                lead_data.company_name,      # Company name
                lead_data.contact_name,      # Contact name
                lead_data.contact_phone,     # Contact phone
                lead_data.contact_email,     # Contact email
                lead_data.additional_info,   # Additional info
                lead_data.status,            # Status
                f"tg://user?id={lead_data.user_id}"  # Telegram link
            ]
            
            # Append row to sheet
            body = {
                'values': [row_data]
            }
            
            result = self.service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range=f"{self.worksheet_name}!A:O",
                valueInputOption='RAW',
                insertDataOption='INSERT_ROWS',
                body=body
            ).execute()
            
            # Get the row number for the lead ID
            updated_range = result.get('updates', {}).get('updatedRange', '')
            lead_id = updated_range.split('!')[1] if '!' in updated_range else "unknown"
            
            log_storage_operation("save_lead", True, lead_id=lead_id)
            logger.info(f"Lead saved to Google Sheets: {lead_id}")
            
            return LeadResponse(
                success=True,
                message="Lead saved successfully",
                lead_id=lead_id
            )
            
        except HttpError as e:
            log_storage_operation("save_lead", False, error=str(e))
            logger.error(f"Google Sheets API error: {e}")
            return LeadResponse(
                success=False,
                message=f"Failed to save lead: {e}"
            )
        except Exception as e:
            log_storage_operation("save_lead", False, error=str(e))
            logger.error(f"Error saving lead to Google Sheets: {e}")
            return LeadResponse(
                success=False,
                message=f"Failed to save lead: {e}"
            )
    
    async def get_lead(self, lead_id: str) -> Optional[LeadData]:
        """Get lead data by ID (row number)."""
        try:
            # Get specific row
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=f"{self.worksheet_name}!A{lead_id}:O{lead_id}"
            ).execute()
            
            values = result.get('values', [])
            if not values or not values[0]:
                return None
            
            row = values[0]
            # Pad row with empty strings if needed
            while len(row) < 15:
                row.append("")
            
            # Parse row data
            lead_data = LeadData(
                user_id=int(row[1]) if row[1] else 0,
                username=row[2] if row[2] else None,
                first_name=row[3] if row[3] else None,
                last_name=row[4] if row[4] else None,
                service_type=row[5],
                budget=row[6],
                timeline=row[7],
                company_name=row[8],
                contact_name=row[9],
                contact_phone=row[10],
                contact_email=row[11],
                additional_info=row[12],
                status=row[13] if row[13] else "new",
                created_at=datetime.fromisoformat(row[0]) if row[0] else datetime.now()
            )
            
            log_storage_operation("get_lead", True, lead_id=lead_id)
            return lead_data
            
        except Exception as e:
            log_storage_operation("get_lead", False, error=str(e), lead_id=lead_id)
            logger.error(f"Error getting lead from Google Sheets: {e}")
            return None
    
    async def get_leads(self, limit: int = 100, offset: int = 0) -> List[LeadData]:
        """Get list of leads."""
        try:
            # Get data from sheet (skip header row)
            start_row = 2 + offset
            end_row = start_row + limit
            
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=f"{self.worksheet_name}!A{start_row}:O{end_row}"
            ).execute()
            
            values = result.get('values', [])
            leads = []
            
            for row in values:
                if len(row) < 15:
                    # Pad row with empty strings
                    while len(row) < 15:
                        row.append("")
                
                try:
                    lead_data = LeadData(
                        user_id=int(row[1]) if row[1] else 0,
                        username=row[2] if row[2] else None,
                        first_name=row[3] if row[3] else None,
                        last_name=row[4] if row[4] else None,
                        service_type=row[5],
                        budget=row[6],
                        timeline=row[7],
                        company_name=row[8],
                        contact_name=row[9],
                        contact_phone=row[10],
                        contact_email=row[11],
                        additional_info=row[12],
                        status=row[13] if row[13] else "new",
                        created_at=datetime.fromisoformat(row[0]) if row[0] else datetime.now()
                    )
                    leads.append(lead_data)
                except Exception as e:
                    logger.warning(f"Error parsing lead row: {e}")
                    continue
            
            log_storage_operation("get_leads", True, count=len(leads))
            return leads
            
        except Exception as e:
            log_storage_operation("get_leads", False, error=str(e))
            logger.error(f"Error getting leads from Google Sheets: {e}")
            return []
    
    async def update_lead_status(self, lead_id: str, status: str) -> bool:
        """Update lead status."""
        try:
            # Update status in column N (14th column, 0-indexed)
            body = {
                'values': [[status]]
            }
            
            self.service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range=f"{self.worksheet_name}!N{lead_id}",
                valueInputOption='RAW',
                body=body
            ).execute()
            
            log_storage_operation("update_lead_status", True, lead_id=lead_id, status=status)
            return True
            
        except Exception as e:
            log_storage_operation("update_lead_status", False, error=str(e), lead_id=lead_id)
            logger.error(f"Error updating lead status in Google Sheets: {e}")
            return False
    
    async def delete_lead(self, lead_id: str) -> bool:
        """Delete lead (not implemented for Google Sheets)."""
        # Google Sheets doesn't support row deletion via API easily
        # Instead, we'll mark the lead as deleted
        return await self.update_lead_status(lead_id, "deleted")

