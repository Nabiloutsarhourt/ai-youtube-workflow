import os
from dotenv import load_dotenv

# Load environment variables from .env file for local development
load_dotenv()

class Config:
    """Configuration class to manage environment variables."""
    
    # API Keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    YOUTUBE_CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET")  # Path to client_secret.json or raw JSON string
    GOOGLE_SHEETS_CREDENTIALS = os.getenv("GOOGLE_SHEETS_CREDENTIALS") # Path to service_account.json or raw JSON string
    VIDEO_API_KEY = os.getenv("VIDEO_API_KEY")
    
    # YouTube Settings
    YOUTUBE_PLAYLIST_ID = os.getenv("YOUTUBE_PLAYLIST_ID")
    YOUTUBE_CATEGORY_ID = os.getenv("YOUTUBE_CATEGORY_ID", "27") # Education
    
    # Google Sheets Settings
    SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
    SHEET_NAME = os.getenv("SHEET_NAME", "Logs")
    
    # Video Generation Settings
    VIDEO_DURATION = int(os.getenv("VIDEO_DURATION", "10")) # seconds
    VIDEO_RESOLUTION = os.getenv("VIDEO_RESOLUTION", "1080p")

    @classmethod
    def validate(cls):
        """Validates that essential configuration is present."""
        missing = []
        if not cls.GEMINI_API_KEY: missing.append("GEMINI_API_KEY")
        if not cls.YOUTUBE_CLIENT_SECRET: missing.append("YOUTUBE_CLIENT_SECRET")
        if not cls.GOOGLE_SHEETS_CREDENTIALS: missing.append("GOOGLE_SHEETS_CREDENTIALS")
        if not cls.VIDEO_API_KEY: missing.append("VIDEO_API_KEY")
        
        if missing:
            raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}")
