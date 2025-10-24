import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2.service_account import Credentials
from app.config import settings
from loguru import logger
import json

scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

sa_info = json.loads(os.environ["GCP_SA_JSON"])

try:
    logger.info("Trying to access google sheets...")
    # creds = ServiceAccountCredentials.from_json_keyfile_name(os.path.join(BASE_DIR,"service_account.json"), scope)
    creds = Credentials.from_service_account_info(sa_info, scopes=scope)
    # client = gspread.authorize(creds)
    client = gspread.authorize(creds)
except Exception as e:
    logger.error(f"Failed to access google sheets: {e}")

# Open your Google Sheet
sheet = client.open_by_key(settings.GOOGLE_SHEETS_SPREADSHEET_ID).sheet1

# sheet = client.open_by_key(settings.GOOGLE_SHEETS_SPREADSHEET_ID).sheet1

async def add_to_sheet(tg_id,first_name, last_name, email,service,description):
    sheet.append_row([tg_id,first_name, last_name, email,service,description])