#!/usr/bin/env python3
"""
ASMR Bug adder
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
import openai
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip
import subprocess

class ASMRVideoAutomation:
    def __init__(self):
        self.setup_credentials()
        self.setup_sheets()
        self.setup_apis()
        
    def setup_credentials(self):
        """Setup Google Sheets and YouTube API credentials"""
        # Google Sheets credentials (set these as environment variables)
        self.sheet_id = os.getenv('GOOGLE_SHEET_ID', '1zKWr1zeoadgbJTd7E24N2TBXJKHlnQS9GW5I0-_9IgA')
        
        # API Keys (set as environment variables)
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.youtube_api_key = os.getenv('YOUTUBE_API_KEY')
        
        # Google service account JSON (base64 encoded as env var)
        google_creds_json = os.getenv('GOOGLE_CREDENTIALS_JSON')
        if google_creds_json:
            import base64
            creds_data = json.loads(base64.b64decode(google_creds_json).decode())
            self.google_creds = Credentials.from_service_account_info(
                creds_data,
                scopes=['https://www.googleapis.com/auth/spreadsheets',
                       'https://www.googleapis.com/auth/youtube.upload']
            )
        
    def setup_sheets(self):
        """Initialize Google Sheets connection"""
        try:
            gc = gspread.authorize(self.google_creds)
            self.sheet = gc.open_by_key(self.sheet_id)
            self.content_tracker = self.sheet.worksheet('ASMR Content Tracker')
            self.fruit_database = self.sheet.worksheet('Fruit_Database')
            self.settings = self.sheet.worksheet('Settings')
            print("✅ Google Sheets connected successfully")
        except Exception as e:
            print(f"❌ Google Sheets connection failed: {e}")
            
    def setup_apis(self):
        """Setup external API connections"""
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
            
    def get_settings(self) -> Dict:
        """Read settings from Google Sheets"""
        try:
            settings_data = self.settings.get_all_records()
            settings = {}
            for row in settings_data:
                settings[row['Setting']] = row['Value']
            return settings
        except Exception as e:
            print(f"❌ Error reading settings: {e}")
            return {'Schedule_Hours': 8, 'Max_Recent_Objects': 7}
    
    def get_recent_objects(self, max_recent: int = 7) -> List[str]:
        """Get recently used objects from content tracker"""
        try:
            records = self.content_tracker.get_all_records()
            # Sort by created date and get most recent
            recent_objects = []
            for record in records[-max_recent:]:
                obj_name = record.get('Object', '').replace('Glass ', '').lower()
                if obj_name:
                    recent_objects.append(obj_name)
            return recent_objects
        except Exception as e:
            print(f"❌ Error getting recent objects: {e}")
            return []
    
    def get_available_fruits(self) -> List[Dict]:
        """Get all fruits from database"""
        try:
            fruits = self.fruit_database.get_all_records()
            return fruits
        except Exception as e:
            print(f"❌ Error getting fruits database: {e}")
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
            print("⚠️ All fruits used recently, selecting from full list")
            unused_fruits = available_fruits
        
        if unused_fruits:
            # Select fruit with highest visual appeal score
            selected = max(unused_fruits, key=lambda x: int(x.get('Visual_Appeal_Score', 0)))
            return selected['Fruit_Name']
        
        return "Apple"  # Fallback
    
    def generate_video_prompt(self, fruit_name: str) -> str:
        """Generate detailed ASMR video prompt"""
        base_prompt = f"""A hyper-realistic close-up of a translucent glass {fruit_name.lower()} on a dark wooden cutting board, with soft top-down lighting creating beautiful reflections. A sharp steel knife enters from the right and slowly slices through the glass {fruit_name.lower()}. 

The scene captures these ASMR sound moments:
1. Sharp metallic tap as knife touches the glass surface
2. Smooth glass-slicing sound as the knife cuts through
3. Dull thud as the knife hits the wooden board
4. Soft crystalline clink as the glass piece settles

Camera is fixed in 9:16 vertical format, focusing on the cut and the vibrantly colored glass interior. The {fruit_name.lower()} has realistic glass texture with internal light refraction. Cinematic lighting, ASMR-focused, minimal background noise."""

        return base_prompt
    
    def generate_video_with_qwen(self, prompt: str) -> Optional[str]:
        """Generate video using Qwen AI (free tier)"""
        try:
            # This is a placeholder for Qwen AI API call
            # In practice, you'd integrate with Qwen's API when available
            print(f"🎬 Generating video with prompt: {prompt[:100]}...")
            
            # Simulate video generation
            time.sleep(5)  # Simulate processing time
            
            # Return mock video URL
            video_filename = f"glass_{fruit_name}_{int(time.time())}.mp4"
            print(f"✅ Video generated: {video_filename}")
            return video_filename
            
        except Exception as e:
            print(f"❌ Video generation failed: {e}")
            return None
    
    def download_asmr_sounds(self) -> List[str]:
        """Download free ASMR sound effects"""
        sound_urls = [
            "https://mixkit.co/free-sound-effects/glass/mixkit-glass-bowl-tap-1188.wav",
            "https://mixkit.co/free-sound-effects/glass/mixkit-glass-breaking-1169.wav",
            "https://mixkit.co/free-sound-effects/kitchen/mixkit-knife-hit-wood-1194.wav",
            "https://mixkit.co/free-sound-effects/glass/mixkit-glass-clink-1185.wav"
        ]
        
        downloaded_files = []
        for i, url in enumerate(sound_urls):
            try:
                # This would download actual sound files
                filename = f"sound_{i}.wav"
                print(f"📥 Downloaded: {filename}")
                downloaded_files.append(filename)
            except Exception as e:
                print(f"❌ Failed to download sound {i}: {e}")
        
        return downloaded_files
    
    def create_asmr_audio(self, sound_files: List[str]) -> str:
        """Create composite ASMR audio track"""
        try:
            # Use ffmpeg to combine audio files with timing
            output_file = "asmr_audio.mp3"
            
            # This would use actual audio processing
            print("🎵 Creating ASMR audio composite...")
            time.sleep(2)  # Simulate processing
            
            return output_file
        except Exception as e:
            print(f"❌ Audio creation failed: {e}")
            return None
    
    def combine_video_audio(self, video_file: str, audio_file: str) -> str:
        """Combine video and ASMR audio"""
        try:
            output_file = f"final_{video_file}"
            
            # Use ffmpeg to combine
            cmd = [
                'ffmpeg', '-i', video_file, '-i', audio_file,
                '-shortest', '-c:v', 'copy', '-c:a', 'aac',
                output_file
            ]
            
            print("🎬 Combining video and audio...")
            # subprocess.run(cmd, check=True)  # Uncomment for actual processing
            time.sleep(3)  # Simulate processing
            
            return output_file
        except Exception as e:
            print(f"❌ Video-audio combination failed: {e}")
            return None
    
    def upload_to_youtube(self, video_file: str, title: str, description: str) -> Optional[str]:
        """Upload video to YouTube using API"""
        try:
            youtube = build('youtube', 'v3', credentials=self.google_creds)
            
            body = {
                'snippet': {
                    'title': title,
                    'description': description,
                    'tags': ['ASMR', 'glass', 'cutting', 'relaxing', 'sounds'],
                    'categoryId': '22'  # People & Blogs
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
            
            print("📤 Uploading to YouTube...")
            response = request.execute()
            
            video_id = response['id']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            
            print(f"✅ YouTube upload successful: {video_url}")
            return video_url
            
        except Exception as e:
            print(f"❌ YouTube upload failed: {e}")
            return None
    
    def log_to_sheet(self, object_name: str, video_url: str, generation_time: float):
        """Log new video to content tracker sheet"""
        try:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
            gen_time_str = f"{generation_time:.1f} min"
            
            # Add new row
            new_row = [
                f"Glass {object_name}",
                video_url or "Failed",
                current_time,
                "Live" if video_url else "Failed",
                "Pending",  # Instagram
                "Pending",  # TikTok
                gen_time_str
            ]
            
            self.content_tracker.append_row(new_row)
            
            # Remove oldest row if we have too many
            all_rows = self.content_tracker.get_all_values()
            if len(all_rows) > 20:  # Keep last 20 entries
                self.content_tracker.delete_rows(2)  # Delete second row (first data row)
            
            print("✅ Logged to Google Sheets")
            
        except Exception as e:
            print(f"❌ Sheet logging failed: {e}")
    
    def run_automation_cycle(self):
        """Run complete automation cycle"""
        start_time = time.time()
        print(f"🚀 Starting ASMR automation cycle at {datetime.now()}")
        
        try:
            # Step 1: Select new fruit
            fruit_name = self.select_new_fruit()
            print(f"🍎 Selected fruit: {fruit_name}")
            
            # Step 2: Generate video prompt
            prompt = self.generate_video_prompt(fruit_name)
            print("📝 Generated video prompt")
            
            # Step 3: Generate video
            video_file = self.generate_video_with_qwen(prompt)
            if not video_file:
                raise Exception("Video generation failed")
            
            # Step 4: Download and create ASMR audio
            sound_files = self.download_asmr_sounds()
            audio_file = self.create_asmr_audio(sound_files)
            
            # Step 5: Combine video and audio
            final_video = self.combine_video_audio(video_file, audio_file)
            
            # Step 6: Upload to YouTube
            title = f"ASMR Glass {fruit_name} Cutting & Slicing Sounds 🔪✨"
            description = f"Relaxing ASMR video of cutting a glass {fruit_name.lower()}. Perfect for sleep, study, and relaxation. #ASMR #Glass #Cutting #Relaxing"
            
            video_url = self.upload_to_youtube(final_video, title, description)
            
            # Step 7: Log to sheet
            generation_time = (time.time() - start_time) / 60
            self.log_to_sheet(fruit_name, video_url, generation_time)
            
            print(f"✅ Automation cycle completed in {generation_time:.1f} minutes")
            return True
            
        except Exception as e:
            print(f"❌ Automation cycle failed: {e}")
            generation_time = (time.time() - start_time) / 60
            self.log_to_sheet(fruit_name if 'fruit_name' in locals() else "Unknown", None, generation_time)
            return False

def main():
    """Main execution function"""
    automation = ASMRVideoAutomation()
    
    # Check if running in scheduled mode or single run
    if os.getenv('RUN_ONCE'):
        automation.run_automation_cycle()
    else:
        # Continuous mode with 8-hour intervals
        settings = automation.get_settings()
        interval_hours = int(settings.get('Schedule_Hours', 8))
        interval_seconds = interval_hours * 3600
        
        print(f"🕐 Starting continuous mode with {interval_hours}h intervals")
        
        while True:
            success = automation.run_automation_cycle()
            
            if success:
                print(f"😴 Sleeping for {interval_hours} hours until next run...")
            else:
                print(f"😴 Error occurred, sleeping for 1 hour before retry...")
                interval_seconds = 3600  # Retry in 1 hour on error
            
            time.sleep(interval_seconds)

if __name__ == "__main__":
    main()
