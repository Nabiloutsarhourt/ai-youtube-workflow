import gspread
from google.oauth2.service_account import Credentials
from config import Config
from utils.logger import logger
import json
from datetime import datetime

class SheetsLogger:
    """Logs execution data to Google Sheets."""

    def __init__(self):
        self.scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        self.creds_info = Config.GOOGLE_SHEETS_CREDENTIALS
        self.spreadsheet_id = Config.SPREADSHEET_ID

    def get_client(self):
        """Returns a gspread client."""
        try:
            if os.path.exists(self.creds_info):
                creds = Credentials.from_service_account_file(self.creds_info, scopes=self.scopes)
            else:
                info = json.loads(self.creds_info)
                creds = Credentials.from_service_account_info(info, scopes=self.scopes)
            return gspread.authorize(creds)
        except Exception as e:
            logger.error(f"Google Sheets Authentication failed: {e}")
            raise

    def log_to_sheets(self, data: dict):
        """
        Appends a row of data to the Google Sheet.
        Expected keys in data: 'prompt', 'title', 'youtube_url', 'execution_status'
        """
        try:
            client = self.get_client()
            sheet = client.open_by_key(self.spreadsheet_id).worksheet(Config.SHEET_NAME)
            
            row = [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                data.get('prompt', ''),
                data.get('title', ''),
                data.get('youtube_url', ''),
                data.get('execution_status', 'SUCCESS')
            ]
            
            sheet.append_row(row)
            logger.info("Successfully logged execution to Google Sheets.")
        except Exception as e:
            logger.error(f"Failed to log to Google Sheets: {e}")
            # We don't raise here to avoid failing the whole workflow if logging fails
import os # Added missing import
