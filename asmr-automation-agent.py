#!/usr/bin/env python3

import os
import json
import time
import random
import base64
from datetime import datetime
from typing import List, Dict, Optional
import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import subprocess
import sys

class ASMRVideoAutomation:
    def __init__(self):
        self.setup_credentials()
        self.setup_sheets()
        
    def setup_credentials(self):
        self.sheet_id = os.getenv('GOOGLE_SHEET_ID')
        self.youtube_api_key = os.getenv('YOUTUBE_API_KEY')
        
        google_creds_json = os.getenv('GOOGLE_CREDENTIALS_JSON')
        if not google_creds_json:
            raise ValueError("GOOGLE_CREDENTIALS_JSON not set")
            
        creds_data = json.loads(base64.b64decode(google_creds_json).decode())
        self.google_creds = Credentials.from_service_account_info(
            creds_data,
            scopes=['https://www.googleapis.com/auth/spreadsheets',
                   'https://www.googleapis.com/auth/youtube.upload']
        )
        
    def setup_sheets(self):
        try:
            gc = gspread.authorize(self.google_creds)
            self.sheet = gc.open_by_key(self.sheet_id)
            self.content_tracker = self.sheet.worksheet('ASMR Content Tracker')
            self.fruit_database = self.sheet.worksheet('Fruit_Database')
            self.settings = self.sheet.worksheet('Settings')
            print("✅ Google Sheets connected")
        except Exception as e:
            print(f"❌ Sheets connection failed: {e}")
            raise
            
    def get_settings(self) -> Dict:
        try:
            settings_data = self.settings.get_all_records()
            return {row['Setting']: row['Value'] for row in settings_data}
        except Exception as e:
            print(f"❌ Settings error: {e}")
            return {'Schedule_Hours': 8, 'Max_Recent_Objects': 7}
    
    def get_recent_objects(self, max_recent: int = 7) -> List[str]:
        try:
            records = self.content_tracker.get_all_records()
            recent_objects = []
            for record in records[-max_recent:]:
                obj_name = record.get('Object', '').replace('Glass ', '').lower()
                if obj_name:
                    recent_objects.append(obj_name)
            return recent_objects
        except Exception as e:
            print(f"❌ Recent objects error: {e}")
            return []
    
    def get_available_fruits(self) -> List[Dict]:
        try:
            return self.fruit_database.get_all_records()
        except Exception as e:
            print(f"❌ Fruits database error: {e}")
            return []
    
    def select_new_fruit(self) -> str:
        settings = self.get_settings()
        max_recent = int(settings.get('Max_Recent_Objects', 7))
        
        recent_objects = self.get_recent_objects(max_recent)
        available_fruits = self.get_available_fruits()
        
        unused_fruits = [fruit for fruit in available_fruits 
                        if fruit.get('Fruit_Name', '').lower() not in recent_objects]
        
        if not unused_fruits:
            unused_fruits = available_fruits
        
        if unused_fruits:
            selected = max(unused_fruits, key=lambda x: int(x.get('Visual_Appeal_Score', 0)))
            return selected['Fruit_Name']
        
        return "Apple"
    
    def create_mock_video(self, fruit_name: str) -> str:
        """Create a simple test video using ffmpeg"""
        try:
            video_filename = f"glass_{fruit_name}_{int(time.time())}.mp4"
            
            # Create a simple colored video with text
            cmd = [
                'ffmpeg', '-y', '-f', 'lavfi', 
                '-i', f'color=c=blue:size=720x1280:duration=10',
                '-vf', f'drawtext=text="Glass {fruit_name} ASMR":fontcolor=white:fontsize=40:x=(w-text_w)/2:y=(h-text_h)/2',
                '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-t', '10',
                video_filename
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"❌ FFmpeg error: {result.stderr}")
                return None
                
            print(f"✅ Mock video created: {video_filename}")
            return video_filename
            
        except Exception as e:
            print(f"❌ Video creation failed: {e}")
            return None
    
    def upload_to_youtube(self, video_file: str, title: str, description: str) -> Optional[str]:
        try:
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
            if len(all_rows) > 21:
                self.content_tracker.delete_rows(2)
            
            print("✅ Logged to Google Sheets")
            
        except Exception as e:
            print(f"❌ Sheet logging failed: {e}")
    
    def run_automation_cycle(self):
        start_time = time.time()
        print(f"🚀 Starting ASMR automation cycle at {datetime.now()}")
        
        try:
            fruit_name = self.select_new_fruit()
            print(f"🍎 Selected fruit: {fruit_name}")
            
            video_file = self.create_mock_video(fruit_name)
            if not video_file:
                raise Exception("Video generation failed")
            
            title = f"ASMR Glass {fruit_name} Cutting & Slicing Sounds 🔪✨"
            description = f"Relaxing ASMR video of cutting a glass {fruit_name.lower()}. Perfect for sleep, study, and relaxation. #ASMR #Glass #Cutting #Relaxing"
            
            video_url = self.upload_to_youtube(video_file, title, description)
            
            generation_time = (time.time() - start_time) / 60
            self.log_to_sheet(fruit_name, video_url, generation_time)
            
            # Cleanup
            if os.path.exists(video_file):
                os.remove(video_file)
            
            print(f"✅ Automation cycle completed in {generation_time:.1f} minutes")
            return True
            
        except Exception as e:
            print(f"❌ Automation cycle failed: {e}")
            generation_time = (time.time() - start_time) / 60
            self.log_to_sheet(fruit_name if 'fruit_name' in locals() else "Unknown", None, generation_time)
            return False

def main():
    try:
        automation = ASMRVideoAutomation()
        success = automation.run_automation_cycle()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
