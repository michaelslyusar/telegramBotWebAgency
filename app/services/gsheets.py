import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from app.config import settings
from loguru import logger

scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]
# Resolve the credentials file path as an absolute path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

try:
    logger.info("Trying to access google sheets...")
    creds = ServiceAccountCredentials.from_json_keyfile_name(os.path.join(BASE_DIR,"service_account.json"), scope)
    client = gspread.authorize(creds)
except Exception as e:
    logger.error(f"Failed to access google sheets: {e}")

# Open your Google Sheet
sheet = client.open_by_key(settings.GOOGLE_SHEETS_SPREADSHEET_ID).sheet1

async def add_to_sheet(tg_id,first_name, last_name, email,service,description):
    sheet.append_row([tg_id,first_name, last_name, email,service,description])