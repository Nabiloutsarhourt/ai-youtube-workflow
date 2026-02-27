from http.server import BaseHTTPRequestHandler
import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import main as run_workflow
from utils.logger import logger

class handler(BaseHTTPRequestHandler):
    """Vercel Serverless Function handler for the daily cron job."""
    
    def do_GET(self):
        logger.info("Triggering AI YouTube Workflow from Vercel Serverless Function...")
        try:
            run_workflow()
            
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write('Workflow executed successfully'.encode('utf-8'))
        except Exception as e:
            logger.error(f"Error in Vercel execution: {e}")
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(f'Workflow failed: {e}'.encode('utf-8'))
