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
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Optional

# Import validation with helpful error messages
def check_imports():
    """Check and import all required dependencies with helpful error messages"""
    missing_modules = []
    
    try:
        import gspread
        print("✅ gspread imported successfully")
    except ImportError:
        missing_modules.append("gspread")
    
    try:
        from google.oauth2.service_account import Credentials
        print("✅ google-auth imported successfully")
    except ImportError:
        missing_modules.append("google-auth")
    
    try:
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
        print("✅ google-api-python-client imported successfully")
    except ImportError:
        missing_modules.append("google-api-python-client")
    
    try:
        from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip
        print("✅ moviepy imported successfully")
    except ImportError:
        missing_modules.append("moviepy")
    
    try:
        import subprocess
        print("✅ subprocess available")
    except ImportError:
        missing_modules.append("subprocess (should be built-in)")
    
    if missing_modules:
        print(f"❌ Missing required modules: {', '.join(missing_modules)}")
        print("Please install missing dependencies:")
        print("pip install " + " ".join(missing_modules))
        sys.exit(1)
    
    return True

# Check imports first
check_imports()

# Now import everything
import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip
import subprocess

# Make OpenAI import optional
try:
    import openai
    OPENAI_AVAILABLE = True
    print("✅ OpenAI available")
except ImportError:
    OPENAI_AVAILABLE = False
    print("⚠️ OpenAI not available - using alternative methods")

class ASMRVideoAutomation:
    def __init__(self):
        print("🔧 Initializing ASMR Video Automation...")
        self.validate_environment()
        self.setup_credentials()
        self.setup_sheets()
        self.setup_apis()
        print("✅ Initialization complete")
        
    def validate_environment(self):
        """Validate required environment variables"""
        required_vars = ['GOOGLE_SHEET_ID', 'GOOGLE_CREDENTIALS_JSON']
        missing_vars = []
        
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
            print("Please set these environment variables in your GitHub repository secrets")
            sys.exit(1)
        
        print("✅ Environment variables validated")
        
    def setup_credentials(self):
        """Setup Google Sheets and YouTube API credentials"""
        try:
            # Google Sheets credentials
            self.sheet_id = os.getenv('GOOGLE_SHEET_ID')
            
            # API Keys
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
                print("✅ Google credentials loaded")
            else:
                raise Exception("GOOGLE_CREDENTIALS_JSON not found")
                
        except Exception as e:
            print(f"❌ Credential setup failed: {e}")
            sys.exit(1)
        
    def setup_sheets(self):
        """Initialize Google Sheets connection"""
        try:
            gc = gspread.authorize(self.google_creds)
            self.sheet = gc.open_by_key(self.sheet_id)
            
            # Try to access each worksheet, create if doesn't exist
            try:
                self.content_tracker = self.sheet.worksheet('ASMR Content Tracker')
            except gspread.WorksheetNotFound:
                print("⚠️ Creating missing 'ASMR Content Tracker' worksheet")
                self.content_tracker = self.sheet.add_worksheet(title='ASMR Content Tracker', rows=100, cols=7)
                headers = ['Object', 'Video_URL', 'Created_Date', 'YouTube_Status', 'Instagram_Status', 'TikTok_Status', 'Generation_Time']
                self.content_tracker.update('A1:G1', [headers])
            
            try:
                self.fruit_database = self.sheet.worksheet('Fruit_Database')
            except gspread.WorksheetNotFound:
                print("⚠️ Creating missing 'Fruit_Database' worksheet")
                self.fruit_database = self.sheet.add_worksheet(title='Fruit_Database', rows=100, cols=3)
                headers = ['Fruit_Name', 'Category', 'Visual_Appeal_Score']
                self.fruit_database.update('A1:C1', [headers])
                # Add some default fruits
                default_fruits = [
                    ['Apple', 'Common', '9'],
                    ['Orange', 'Citrus', '8'],
                    ['Strawberry', 'Berry', '10'],
                    ['Mango', 'Tropical', '10'],
                    ['Grape', 'Berry', '9']
                ]
                self.fruit_database.update('A2:C6', default_fruits)
            
            try:
                self.settings = self.sheet.worksheet('Settings')
            except gspread.WorksheetNotFound:
                print("⚠️ Creating missing 'Settings' worksheet")
                self.settings = self.sheet.add_worksheet(title='Settings', rows=20, cols=3)
                headers = ['Setting', 'Value', 'Description']
                self.settings.update('A1:C1', [headers])
                default_settings = [
                    ['Schedule_Hours', '8', 'Hours between automated runs'],
                    ['Max_Recent_Objects', '7', 'Number of recent objects to avoid']
                ]
                self.settings.update('A2:C3', default_settings)
            
            print("✅ Google Sheets connected successfully")
            
        except Exception as e:
            print(f"❌ Google Sheets connection failed: {e}")
            sys.exit(1)
            
    def setup_apis(self):
        """Setup external API connections"""
        if OPENAI_AVAILABLE and self.openai_api_key:
            openai.api_key = self.openai_api_key
            print("✅ OpenAI API configured")
        else:
            print("⚠️ OpenAI API not available")
            
    def get_settings(self) -> Dict:
        """Read settings from Google Sheets"""
        try:
            settings_data = self.content_tracker.get_all_records()
            settings = {}
            for row in settings_data:
                if 'Setting' in row and 'Value' in row:
                    settings[row['Setting']] = row['Value']
            return settings
        except Exception as e:
            print(f"❌ Error reading settings: {e}")
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
            print(f"📋 Recently used objects: {recent_objects}")
            return recent_objects
        except Exception as e:
            print(f"❌ Error getting recent objects: {e}")
            return []
    
    def get_available_fruits(self) -> List[Dict]:
        """Get all fruits from database"""
        try:
            fruits = self.fruit_database.get_all_records()
            print(f"🍎 Available fruits in database: {len(fruits)}")
            return fruits
        except Exception as e:
            print(f"❌ Error getting fruits database: {e}")
            return [{'Fruit_Name': 'Apple', 'Category': 'Common', 'Visual_Appeal_Score': '9'}]
    
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
            fruit_name = selected['Fruit_Name']
            print(f"🎯 Selected fruit: {fruit_name}")
            return fruit_name
        
        print("⚠️ Using fallback fruit: Apple")
        return "Apple"
    
    def generate_video_prompt(self, fruit_name: str) -> str:
        """Generate detailed ASMR video prompt"""
        colors = {
            'apple': 'red and green',
            'orange': 'bright orange',
            'strawberry': 'red with green top',
            'grape': 'deep purple',
            'mango': 'golden yellow-orange',
            'banana': 'bright yellow',
            'kiwi': 'brown exterior with green interior',
            'peach': 'pink and yellow'
        }
        
        color = colors.get(fruit_name.lower(), 'vibrant colored')
        
        base_prompt = f"""A hyper-realistic close-up of a translucent glass {fruit_name.lower()} with {color} tints on a dark wooden cutting board, with soft top-down lighting creating beautiful reflections. A sharp steel knife enters from the right and slowly slices through the glass {fruit_name.lower()}. 

The scene captures these ASMR sound moments:
1. Sharp metallic tap as knife touches the glass surface
2. Smooth glass-slicing sound as the knife cuts through
3. Dull thud as the knife hits the wooden board
4. Soft crystalline clink as the glass piece settles

Camera is fixed in 9:16 vertical format, focusing on the cut and the vibrantly colored glass interior. The {fruit_name.lower()} has realistic glass texture with internal light refraction. Cinematic lighting, ASMR-focused, minimal background noise."""

        print(f"📝 Generated video prompt for {fruit_name}")
        return base_prompt
    
    def generate_video_with_placeholder(self, prompt: str, fruit_name: str) -> Optional[str]:
        """Generate video using placeholder method (replace with actual AI service)"""
        try:
            print(f"🎬 Generating video with prompt: {prompt[:100]}...")
            print("⚠️ This is a placeholder - integrate with actual AI video service")
            
            # Simulate video generation
            time.sleep(5)
            
            # Return mock video filename
            video_filename = f"glass_{fruit_name.lower()}_{int(time.time())}.mp4"
            print(f"✅ Video generated: {video_filename}")
            return video_filename
            
        except Exception as e:
            print(f"❌ Video generation failed: {e}")
            return None
    
    def create_placeholder_asmr_audio(self) -> str:
        """Create placeholder ASMR audio track"""
        try:
            print("🎵 Creating placeholder ASMR audio...")
            print("⚠️ This is a placeholder - integrate with actual audio processing")
            
            # Simulate audio creation
            time.sleep(2)
            
            output_file = "asmr_audio.mp3"
            print(f"✅ Audio created: {output_file}")
            return output_file
            
        except Exception as e:
            print(f"❌ Audio creation failed: {e}")
            return None
    
    def log_to_sheet(self, object_name: str, video_url: Optional[str], generation_time: float):
        """Log new video to content tracker sheet"""
        try:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
            gen_time_str = f"{generation_time:.1f} min"
            
            # Add new row
            new_row = [
                f"Glass {object_name}",
                video_url or "Generation Failed",
                current_time,
                "Placeholder" if video_url else "Failed",
                "Pending",
                "Pending",
                gen_time_str
            ]
            
            self.content_tracker.append_row(new_row)
            
            # Keep only last 20 entries
            all_rows = self.content_tracker.get_all_values()
            if len(all_rows) > 21:  # 20 + header
                rows_to_delete = len(all_rows) - 21
                for _ in range(rows_to_delete):
                    self.content_tracker.delete_rows(2)  # Delete second row
            
            print("✅ Logged to Google Sheets")
            
        except Exception as e:
            print(f"❌ Sheet logging failed: {e}")
    
    def run_automation_cycle(self):
        """Run complete automation cycle"""
        start_time = time.time()
        print(f"🚀 Starting ASMR automation cycle at {datetime.now()}")
        
        fruit_name = None
        try:
            # Step 1: Select new fruit
            fruit_name = self.select_new_fruit()
            print(f"🍎 Selected fruit: {fruit_name}")
            
            # Step 2: Generate video prompt
            prompt = self.generate_video_prompt(fruit_name)
            print("📝 Generated video prompt")
            
            # Step 3: Generate video (placeholder)
            video_file = self.generate_video_with_placeholder(prompt, fruit_name)
            if not video_file:
                raise Exception("Video generation failed")
            
            # Step 4: Create ASMR audio (placeholder)
            audio_file = self.create_placeholder_asmr_audio()
            
            # Step 5: Log success
            generation_time = (time.time() - start_time) / 60
            video_url = f"https://placeholder-video-url.com/{video_file}"
            self.log_to_sheet(fruit_name, video_url, generation_time)
            
            print(f"✅ Automation cycle completed in {generation_time:.1f} minutes")
            return True
            
        except Exception as e:
            print(f"❌ Automation cycle failed: {e}")
            generation_time = (time.time() - start_time) / 60
            self.log_to_sheet(fruit_name or "Unknown", None, generation_time)
            return False

def main():
    """Main execution function"""
    try:
        automation = ASMRVideoAutomation()
        
        # Check if running in scheduled mode or single run
        if os.getenv('RUN_ONCE'):
            print("🎯 Running single automation cycle")
            success = automation.run_automation_cycle()
            sys.exit(0 if success else 1)
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
                    interval_seconds = 3600
                
                time.sleep(interval_seconds)
                
    except KeyboardInterrupt:
        print("\n⏹️ Automation stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
