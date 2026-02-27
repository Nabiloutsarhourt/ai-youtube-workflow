# AI YouTube Workflow

Fully autonomous AI system that generates AI construction timelapse videos and publishes them to YouTube daily.

## 🚀 Features
- **Auto-prompting**: Uses Gemini 1.5 Flash to create video prompts and SEO-optimized YouTube metadata.
- **Auto-video**: Integrated with Video Generation APIs (placeholder included).
- **Auto-upload**: Seamlessly uploads to YouTube using Data API v3.
- **Auto-logging**: Appends execution logs to Google Sheets for tracking.
- **Zero-touch**: Runs completely on GitHub Actions.

## 🛠 Setup Instructions

### 1. API Keys & Credentials
- **Gemini API**: Get your key from [Google AI Studio](https://aistudio.google.com/).
- **YouTube API**: Enable YouTube Data API v3 in Google Cloud Console. Create OAuth2 credentials and obtain a Refresh Token.
- **Google Sheets API**: Create a Service Account, download the JSON key, and share your spreadsheet with the service account email.
- **Video API**: Obtain an API key from your preferred provider (Runway, Pika, etc.).

### 2. GitHub Secrets
Add the following secrets to your GitHub repository (`Settings > Secrets and variables > Actions`):
- `GEMINI_API_KEY`
- `YOUTUBE_CLIENT_SECRET`: Your OAuth2 authorized user JSON (including refresh token).
- `GOOGLE_SHEETS_CREDENTIALS`: Your Service Account JSON.
- `VIDEO_API_KEY`
- `SPREADSHEET_ID`: The ID from your Google Sheet URL.

## 📁 Project Structure
- `main.py`: The orchestrator.
- `gemini_generator.py`: Content generation.
- `video_generator.py`: Video generation.
- `youtube_uploader.py`: YouTube integration.
- `sheets_logger.py`: Google Sheets integration.
- `config.py`: Configuration management.
- `.github/workflows/automation.yml`: CI/CD schedule.
- `api/cron.py` & `vercel.json`: Vercel Serverless Function setup.

## 🚀 Deployment Options

### Option 1: GitHub Actions (Default)
The workflow runs automatically every day at 12:00 PM UTC via `.github/workflows/automation.yml`. You can also trigger it manually from the "Actions" tab.

### Option 2: Vercel Serverless
This project includes an optimized version for Vercel Serverless deployment using Vercel Cron Jobs:
1. Import the repository into Vercel.
2. In the Vercel project settings, add all the API keys and credentials as Environment Variables.
3. Vercel will automatically detect `vercel.json` and `api/cron.py` and schedule the daily execution.

## ⚖️ License
MIT
