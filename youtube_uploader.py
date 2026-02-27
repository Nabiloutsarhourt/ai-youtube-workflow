import os
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload
from config import Config
from utils.logger import logger
import json

class YouTubeUploader:
    """Handles video uploads to YouTube via Data API v3."""

    def __init__(self):
        self.scopes = ["https://www.googleapis.com/auth/youtube.upload"]
        self.api_service_name = "youtube"
        self.api_version = "v3"
        self.client_secrets_file = Config.YOUTUBE_CLIENT_SECRET # Path or string

    def get_authenticated_service(self):
        """Authenticates and returns the YouTube service object."""
        # Note: In a GitHub Action, we usually use a Refresh Token stored in Secrets
        # for a non-interactive flow. This implementation assumes Config.YOUTUBE_CLIENT_SECRET
        # is a path to a credentials JSON or the JSON itself.
        
        try:
            if os.path.exists(self.client_secrets_file):
                # Local flow for initial setup
                flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                    self.client_secrets_file, self.scopes)
                credentials = flow.run_local_server(port=0)
            else:
                # Production/Action flow using existing credentials from env
                # This would typically be a refresh token flow
                creds_data = json.loads(self.client_secrets_file)
                credentials = google.oauth2.credentials.Credentials.from_authorized_user_info(creds_data, self.scopes)

            return googleapiclient.discovery.build(
                self.api_service_name, self.api_version, credentials=credentials)
        except Exception as e:
            logger.error(f"YouTube Authentication failed: {e}")
            raise

    def upload_video(self, video_path: str, title: str, description: str, tags: list):
        """Uploads a video file to YouTube."""
        youtube = self.get_authenticated_service()
        
        body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
                "categoryId": Config.YOUTUBE_CATEGORY_ID
            },
            "status": {
                "privacyStatus": "public",
                "selfDeclaredMadeForKids": False,
            }
        }

        media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
        
        logger.info(f"Starting upload of '{title}'...")
        request = youtube.videos().insert(
            part="snippet,status",
            body=body,
            media_body=media
        )

        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                logger.info(f"Uploaded {int(status.progress() * 100)}%")

        video_id = response.get("id")
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        logger.info(f"Upload successful! Video URL: {video_url}")
        return video_url
