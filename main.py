import sys
from config import Config
from utils.logger import logger
from gemini_generator import GeminiGenerator
from video_generator import VideoGenerator
from youtube_uploader import YouTubeUploader
from sheets_logger import SheetsLogger

def main():
    logger.info("--- Starting AI YouTube Workflow ---")
    
    try:
        # 1. Validate Configuration
        Config.validate()
        
        # 2. Initialize Components
        gemini = GeminiGenerator()
        video_gen = VideoGenerator()
        uploader = YouTubeUploader()
        sheets = SheetsLogger()
        
        # 3. Generate Content & Metadata
        logger.info("Step 1: Generating content and metadata...")
        content = gemini.generate_content(domain="Construction Timelapse")
        prompt = content.get('video_prompt')
        title = content.get('youtube_title')
        description = content.get('youtube_description')
        tags = content.get('youtube_tags', [])
        
        # 4. Generate Video
        logger.info("Step 2: Generating video file...")
        video_path = video_gen.generate_video(prompt)
        
        # 5. Upload to YouTube
        logger.info("Step 3: Uploading to YouTube...")
        youtube_url = uploader.upload_video(video_path, title, description, tags)
        
        # 6. Log to Google Sheets
        logger.info("Step 4: Logging execution...")
        log_data = {
            'prompt': prompt,
            'title': title,
            'youtube_url': youtube_url,
            'execution_status': 'SUCCESS'
        }
        sheets.log_to_sheets(log_data)
        
        # 7. Cleanup
        video_gen.cleanup()
        
        logger.info("--- Workflow Completed Successfully ---")

    except Exception as e:
        logger.error(f"Workflow failed: {e}")
        # Log failure to sheets if possible
        try:
            sheets = SheetsLogger()
            sheets.log_to_sheets({
                'prompt': 'N/A',
                'title': 'ERROR',
                'youtube_url': 'N/A',
                'execution_status': f"FAILED: {str(e)}"
            })
        except:
            pass
        raise e  # Raise instead of sys.exit so the Serverless function can catch it

if __name__ == "__main__":
    try:
        main()
    except Exception:
        sys.exit(1)
