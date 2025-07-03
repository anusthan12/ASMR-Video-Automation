#!/usr/bin/env python3
"""
ASMR Video Automation Agent
Generates glass fruit ASMR videos every 8 hours using free AI tools
"""

import os
import json
import time
import random
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import subprocess
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ASMRVideoAutomation:
    def __init__(self):
        self.setup_credentials()
        self.setup_sheets()
        
    def setup_credentials(self):
        """Setup Google Sheets and YouTube API credentials"""
        try:
            # Google Sheets credentials (set these as environment variables)
            self.sheet_id = os.getenv('GOOGLE_SHEET_ID')
            if not self.sheet_id:
                raise ValueError("GOOGLE_SHEET_ID environment variable not set")
            
            # API Keys (set as environment variables)
            self.youtube_api_key = os.getenv('YOUTUBE_API_KEY')
            
            # Google service account JSON (base64 encoded as env var)
            google_creds_json = os.getenv('GOOGLE_CREDENTIALS_JSON')
            if not google_creds_json:
                raise ValueError("GOOGLE_CREDENTIALS_JSON environment variable not set")
            
            import base64
            creds_data = json.loads(base64.b64decode(google_creds_json).decode())
            self.google_creds = Credentials.from_service_account_info(
                creds_data,
                scopes=['https://www.googleapis.com/auth/spreadsheets',
                       'https://www.googleapis.com/auth/youtube.upload']
            )
            logger.info("✅ Credentials setup successful")
            
        except Exception as e:
            logger.error(f"❌ Credentials setup failed: {e}")
            raise
        
    def setup_sheets(self):
        """Initialize Google Sheets connection"""
        try:
            gc = gspread.authorize(self.google_creds)
            self.sheet = gc.open_by_key(self.sheet_id)
            
            # Try to get worksheets, create if they don't exist
            try:
                self.content_tracker = self.sheet.worksheet('ASMR Content Tracker')
            except gspread.WorksheetNotFound:
                self.content_tracker = self.sheet.add_worksheet(title='ASMR Content Tracker', rows=100, cols=7)
                self._setup_content_tracker_headers()
            
            try:
                self.fruit_database = self.sheet.worksheet('Fruit_Database')
            except gspread.WorksheetNotFound:
                self.fruit_database = self.sheet.add_worksheet(title='Fruit_Database', rows=100, cols=3)
                self._setup_fruit_database()
            
            try:
                self.settings = self.sheet.worksheet('Settings')
            except gspread.WorksheetNotFound:
                self.settings = self.sheet.add_worksheet(title='Settings', rows=20, cols=3)
                self._setup_settings()
            
            logger.info("✅ Google Sheets connected successfully")
            
        except Exception as e:
            logger.error(f"❌ Google Sheets connection failed: {e}")
            raise
    
    def _setup_content_tracker_headers(self):
        """Setup headers for content tracker"""
        headers = ['Object', 'Video_URL', 'Created_Date', 'YouTube_Status', 'Instagram_Status', 'TikTok_Status', 'Generation_Time']
        self.content_tracker.update('A1:G1', [headers])
    
    def _setup_fruit_database(self):
        """Setup fruit database with sample data"""
        headers = ['Fruit_Name', 'Category', 'Visual_Appeal_Score']
        self.fruit_database.update('A1:C1', [headers])
        
        fruits = [
            ['Apple', 'Common', '9'],
            ['Orange', 'Citrus', '8'],
            ['Strawberry', 'Berry', '10'],
            ['Banana', 'Tropical', '7'],
            ['Grape', 'Berry', '9'],
            ['Mango', 'Tropical', '10'],
            ['Pineapple', 'Tropical', '9'],
            ['Watermelon', 'Melon', '8'],
            ['Peach', 'Stone', '9'],
            ['Pear', 'Common', '8']
        ]
        self.fruit_database.update('A2:C11', fruits)
    
    def _setup_settings(self):
        """Setup settings with default values"""
        headers = ['Setting', 'Value', 'Description']
        self.settings.update('A1:C1', [headers])
        
        settings = [
            ['Schedule_Hours', '8', 'Hours between automated runs'],
            ['Max_Recent_Objects', '7', 'Number of recent objects to avoid'],
            ['Video_Duration_Seconds', '60', 'Target video duration']
        ]
        self.settings.update('A2:C4', settings)
            
    def get_settings(self) -> Dict:
        """Read settings from Google Sheets"""
        try:
            settings_data = self.settings.get_all_records()
            settings = {}
            for row in settings_data:
                settings[row['Setting']] = row['Value']
            return settings
        except Exception as e:
            logger.error(f"❌ Error reading settings: {e}")
            return {'Schedule_Hours': 8, 'Max_Recent_Objects': 7}
    
    def get_recent_objects(self, max_recent: int = 7) -> List[str]:
        """Get recently used objects from content tracker"""
        try:
            records = self.content_tracker.get_all_records()
            recent_objects = []
            for record in records[-max_recent:]:
                obj_name = record.get('Object', '').replace('Glass ', '').lower()
                if obj_name:
                    recent_objects.append(obj_name)
            return recent_objects
        except Exception as e:
            logger.error(f"❌ Error getting recent objects: {e}")
            return []
    
    def get_available_fruits(self) -> List[Dict]:
        """Get all fruits from database"""
        try:
            fruits = self.fruit_database.get_all_records()
            return fruits
        except Exception as e:
            logger.error(f"❌ Error getting fruits database: {e}")
            return []
    
    def select_new_fruit(self) -> str:
        """Select a new fruit that hasn't been used recently"""
        settings = self.get_settings()
        max_recent = int(settings.get('Max_Recent_Objects', 7))
        
        recent_objects = self.get_recent_objects(max_recent)
        available_fruits = self.get_available_fruits()
        
        # Filter out recently used fruits
        unused_fruits = []
        for fruit in available_fruits:
            fruit_name = fruit.get('Fruit_Name', '').lower()
            if fruit_name not in recent_objects:
                unused_fruits.append(fruit)
        
        if not unused_fruits:
            logger.warning("⚠️ All fruits used recently, selecting from full list")
            unused_fruits = available_fruits
        
        if unused_fruits:
            selected = max(unused_fruits, key=lambda x: int(x.get('Visual_Appeal_Score', 0)))
            return selected['Fruit_Name']
        
        return "Apple"  # Fallback
    
    def generate_video_prompt(self, fruit_name: str) -> str:
        """Generate detailed ASMR video prompt"""
        prompt = f"""A hyper-realistic close-up of a translucent glass {fruit_name.lower()} on a dark wooden cutting board, with soft top-down lighting creating beautiful reflections. A sharp steel knife enters from the right and slowly slices through the glass {fruit_name.lower()}. 

The scene captures these ASMR sound moments:
1. Sharp metallic tap as knife touches the glass surface
2. Smooth glass-slicing sound as the knife cuts through
3. Dull thud as the knife hits the wooden board
4. Soft crystalline clink as the glass piece settles

Camera is fixed in 9:16 vertical format, focusing on the cut and the vibrantly colored glass interior. The {fruit_name.lower()} has realistic glass texture with internal light refraction. Cinematic lighting, ASMR-focused, minimal background noise."""

        return prompt
    
    def create_mock_video(self, fruit_name: str) -> str:
        """Create a mock video file for testing"""
        try:
            video_filename = f"glass_{fruit_name.lower()}_{int(time.time())}.mp4"
            
            # Create a simple test video using ffmpeg
            cmd = [
                'ffmpeg', '-f', 'lavfi', '-i', 'color=c=black:s=1080x1920:d=10',
                '-vf', f'drawtext=text="Glass {fruit_name}":fontsize=60:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2',
                '-t', '10', '-y', video_filename
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                logger.error(f"❌ FFmpeg error: {result.stderr}")
                return None
            
            logger.info(f"✅ Mock video created: {video_filename}")
            return video_filename
            
        except Exception as e:
            logger.error(f"❌ Mock video creation failed: {e}")
            return None
    
    def create_mock_audio(self) -> str:
        """Create mock ASMR audio"""
        try:
            audio_filename = "asmr_audio.mp3"
            
            # Create a simple audio file using ffmpeg
            cmd = [
                'ffmpeg', '-f', 'lavfi', '-i', 'anullsrc=channel_layout=stereo:sample_rate=44100',
                '-t', '10', '-y', audio_filename
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                logger.error(f"❌ FFmpeg audio error: {result.stderr}")
                return None
            
            logger.info(f"✅ Mock audio created: {audio_filename}")
            return audio_filename
            
        except Exception as e:
            logger.error(f"❌ Mock audio creation failed: {e}")
            return None
    
    def combine_video_audio(self, video_file: str, audio_file: str) -> str:
        """Combine video and ASMR audio"""
        try:
            output_file = f"final_{video_file}"
            
            cmd = [
                'ffmpeg', '-i', video_file, '-i', audio_file,
                '-shortest', '-c:v', 'copy', '-c:a', 'aac',
                '-y', output_file
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                logger.error(f"❌ FFmpeg combine error: {result.stderr}")
                return None
            
            logger.info(f"✅ Video and audio combined: {output_file}")
            return output_file
            
        except Exception as e:
            logger.error(f"❌ Video-audio combination failed: {e}")
            return None
    
    def upload_to_youtube(self, video_file: str, title: str, description: str) -> Optional[str]:
        """Upload video to YouTube using API"""
        try:
            if not self.youtube_api_key:
                logger.warning("⚠️ YouTube API key not provided, skipping upload")
                return f"mock_youtube_url_{int(time.time())}"
            
            youtube = build('youtube', 'v3', credentials=self.google_creds)
            
            body = {
                'snippet': {
                    'title': title,
                    'description': description,
                    'tags': ['ASMR', 'glass', 'cutting', 'relaxing', 'sounds'],
                    'categoryId': '22'
                },
                'status': {
                    'privacyStatus': 'public',
                    'selfDeclaredMadeForKids': False
                }
            }
            
            media = MediaFileUpload(video_file, chunksize=-1, resumable=True)
            
            request = youtube.videos().insert(
                part='snippet,status',
                body=body,
                media_body=media
            )
            
            logger.info("📤 Uploading to YouTube...")
            response = request.execute()
            
            video_id = response['id']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            
            logger.info(f"✅ YouTube upload successful: {video_url}")
            return video_url
            
        except Exception as e:
            logger.error(f"❌ YouTube upload failed: {e}")
            return None
    
    def log_to_sheet(self, object_name: str, video_url: str, generation_time: float):
        """Log new video to content tracker sheet"""
        try:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
            gen_time_str = f"{generation_time:.1f} min"
            
            new_row = [
                f"Glass {object_name}",
                video_url or "Failed",
                current_time,
                "Live" if video_url else "Failed",
                "Pending",
                "Pending",
                gen_time_str
            ]
            
            self.content_tracker.append_row(new_row)
            
            # Keep only last 20 entries
            all_rows = self.content_tracker.get_all_values()
            if len(all_rows) > 21:  # 20 data rows + 1 header
                self.content_tracker.delete_rows(2)
            
            logger.info("✅ Logged to Google Sheets")
            
        except Exception as e:
            logger.error(f"❌ Sheet logging failed: {e}")
    
    def cleanup_files(self, files: List[str]):
        """Clean up temporary files"""
        for file in files:
            try:
                if os.path.exists(file):
                    os.remove(file)
                    logger.info(f"🗑️ Cleaned up: {file}")
            except Exception as e:
                logger.error(f"❌ Failed to cleanup {file}: {e}")
    
    def run_automation_cycle(self):
        """Run complete automation cycle"""
        start_time = time.time()
        files_to_cleanup = []
        fruit_name = "Unknown"
        
        try:
            logger.info(f"🚀 Starting ASMR automation cycle at {datetime.now()}")
            
            # Step 1: Select new fruit
            fruit_name = self.select_new_fruit()
            logger.info(f"🍎 Selected fruit: {fruit_name}")
            
            # Step 2: Generate video prompt
            prompt = self.generate_video_prompt(fruit_name)
            logger.info("📝 Generated video prompt")
            
            # Step 3: Create mock video (replace with actual AI generation)
            video_file = self.create_mock_video(fruit_name)
            if not video_file:
                raise Exception("Video creation failed")
            files_to_cleanup.append(video_file)
            
            # Step 4: Create mock audio
            audio_file = self.create_mock_audio()
            if not audio_file:
                raise Exception("Audio creation failed")
            files_to_cleanup.append(audio_file)
            
            # Step 5: Combine video and audio
            final_video = self.combine_video_audio(video_file, audio_file)
            if not final_video:
                raise Exception("Video-audio combination failed")
            files_to_cleanup.append(final_video)
            
            # Step 6: Upload to YouTube
            title = f"ASMR Glass {fruit_name} Cutting & Slicing Sounds 🔪✨"
            description = f"Relaxing ASMR video of cutting a glass {fruit_name.lower()}. Perfect for sleep, study, and relaxation. #ASMR #Glass #Cutting #Relaxing"
            
            video_url = self.upload_to_youtube(final_video, title, description)
            
            # Step 7: Log to sheet
            generation_time = (time.time() - start_time) / 60
            self.log_to_sheet(fruit_name, video_url, generation_time)
            
            logger.info(f"✅ Automation cycle completed in {generation_time:.1f} minutes")
            return True
            
        except Exception as e:
            logger.error(f"❌ Automation cycle failed: {e}")
            generation_time = (time.time() - start_time) / 60
            self.log_to_sheet(fruit_name, None, generation_time)
            return False
        
        finally:
            # Cleanup temporary files
            self.cleanup_files(files_to_cleanup)

def main():
    """Main execution function"""
    try:
        automation = ASMRVideoAutomation()
        
        if os.getenv('RUN_ONCE', '').lower() == 'true':
            logger.info("🔄 Running in single execution mode")
            success = automation.run_automation_cycle()
            if success:
                logger.info("🎉 Automation completed successfully")
            else:
                logger.error("💥 Automation failed")
                exit(1)
        else:
            logger.info("🔄 Running in continuous mode")
            settings = automation.get_settings()
            interval_hours = int(settings.get('Schedule_Hours', 8))
            interval_seconds = interval_hours * 3600
            
            while True:
                success = automation.run_automation_cycle()
                
                if success:
                    logger.info(f"😴 Sleeping for {interval_hours} hours until next run...")
                    time.sleep(interval_seconds)
                else:
                    logger.info("😴 Error occurred, sleeping for 1 hour before retry...")
                    time.sleep(3600)
                    
    except Exception as e:
        logger.error(f"💥 Fatal error: {e}")
        exit(1)

if __name__ == "__main__":
    main()
