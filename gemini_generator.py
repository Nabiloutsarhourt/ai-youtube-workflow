import google.generativeai as genai
import json
from config import Config
from utils.logger import logger

class GeminiGenerator:
    """Wrapper for Google Gemini API to generate content."""

    def __init__(self):
        if not Config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not set in environment.")
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def generate_content(self, domain: str = "Construction Timelapse"):
        """Generates video prompt and YouTube metadata."""
        prompt = (
            f"Generate a creative and detailed text-to-video prompt for an AI video generation tool focusing on '{domain}'. "
            "Also provide a catchy YouTube title, description, and relevant tags. "
            "Return the response in JSON format with keys: 'video_prompt', 'youtube_title', 'youtube_description', 'youtube_tags'."
        )

        try:
            logger.info("Generating content from Gemini...")
            response = self.model.generate_content(prompt)
            # Find JSON in response text (Gemini sometimes adds markdown wrappers)
            text = response.text
            start = text.find('{')
            end = text.rfind('}') + 1
            json_content = json.loads(text[start:end])
            
            logger.info(f"Successfully generated metadata for: {json_content.get('youtube_title')}")
            return json_content
        except Exception as e:
            logger.error(f"Error generating content from Gemini: {e}")
            raise

    def generate_prompt(self):
        content = self.generate_content()
        return content.get('video_prompt')

    def generate_metadata(self):
        content = self.generate_content()
        return {
            'title': content.get('youtube_title'),
            'description': content.get('youtube_description'),
            'tags': content.get('youtube_tags')
        }
