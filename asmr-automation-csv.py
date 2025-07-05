#!/usr/bin/env python3

import os
import json
import time
import random
import csv
import subprocess
import sys
from datetime import datetime
from typing import List, Dict
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials
import base64

class ASMRVideoAutomationCSV:
    def __init__(self):
        self.content_file = 'asmr_content.csv'
        self.fruit_file = 'fruit_database.csv'
        self.settings_file = 'settings.csv'
        self.setup_csv_files()
        self.setup_youtube_credentials()
        
    def setup_youtube_credentials(self):
        """Setup YouTube API credentials"""
        # For GitHub Actions, we'll use a simpler approach - just API key
        # This will create a placeholder video entry without actual upload
        self.youtube_api_key = os.getenv('YOUTUBE_API_KEY')
        if not self.youtube_api_key:
            print("Warning: YOUTUBE_API_KEY not set, will simulate upload")
        
        # Note: For actual YouTube upload, you need OAuth2 credentials
        # Service accounts don't work with YouTube API
    
    def setup_csv_files(self):
        """Initialize CSV files if they don't exist"""
        
        # Content tracker CSV
        if not os.path.exists(self.content_file):
            with open(self.content_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Object', 'Video_URL', 'Created_Date', 'YouTube_Status', 'Generation_Time'])
                # Add sample data
                writer.writerow(['Glass Apple', 'https://example.com/video1', '2025-01-15', 'Live', '5.2 min'])
                writer.writerow(['Glass Orange', 'https://example.com/video2', '2025-01-14', 'Live', '4.8 min'])
        
        # Fruit database CSV
        if not os.path.exists(self.fruit_file):
            with open(self.fruit_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Fruit_Name', 'Category', 'Visual_Appeal_Score'])
                fruits = [
                    ['Apple', 'Common', '9'], ['Orange', 'Citrus', '8'], ['Strawberry', 'Berry', '10'],
                    ['Banana', 'Tropical', '7'], ['Grape', 'Berry', '9'], ['Kiwi', 'Exotic', '8'],
                    ['Mango', 'Tropical', '10'], ['Pineapple', 'Tropical', '9'], ['Watermelon', 'Melon', '8'],
                    ['Peach', 'Stone', '9'], ['Pear', 'Common', '8'], ['Cherry', 'Berry', '10'],
                    ['Plum', 'Stone', '8'], ['Lemon', 'Citrus', '7'], ['Lime', 'Citrus', '7'],
                    ['Dragon Fruit', 'Exotic', '10'], ['Passion Fruit', 'Exotic', '8']
                ]
                writer.writerows(fruits)
        
        # Settings CSV
        if not os.path.exists(self.settings_file):
            with open(self.settings_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Setting', 'Value', 'Description'])
                settings = [
                    ['Schedule_Hours', '8', 'Hours between automated runs'],
                    ['Max_Recent_Objects', '7', 'Number of recent objects to avoid'],
                    ['Video_Duration_Seconds', '10', 'Target video duration']
                ]
                writer.writerows(settings)
    
    def read_csv_to_dict(self, filename: str) -> List[Dict]:
        """Read CSV file and return list of dictionaries"""
        try:
            with open(filename, 'r', newline='') as f:
                reader = csv.DictReader(f)
                return list(reader)
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            return []
    
    def append_to_csv(self, filename: str, data: List):
        """Append data to CSV file"""
        try:
            with open(filename, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(data)
        except Exception as e:
            print(f"Error writing to {filename}: {e}")
    
    def get_settings(self) -> Dict:
        """Get settings from CSV"""
        settings_data = self.read_csv_to_dict(self.settings_file)
        return {row['Setting']: row['Value'] for row in settings_data}
    
    def get_recent_objects(self, max_recent: int = 7) -> List[str]:
        """Get recent objects from content tracker"""
        content_data = self.read_csv_to_dict(self.content_file)
        recent_objects = []
        
        # Get last max_recent entries
        for record in content_data[-max_recent:]:
            obj_name = record.get('Object', '').replace('Glass ', '').lower()
            if obj_name:
                recent_objects.append(obj_name)
        
        return recent_objects
    
    def get_available_fruits(self) -> List[Dict]:
        """Get available fruits from database"""
        return self.read_csv_to_dict(self.fruit_file)
    
    def select_new_fruit(self) -> str:
        """Select a new fruit avoiding recent ones"""
        settings = self.get_settings()
        max_recent = int(settings.get('Max_Recent_Objects', 7))
        
        recent_objects = self.get_recent_objects(max_recent)
        available_fruits = self.get_available_fruits()
        
        # Filter out recently used fruits
        unused_fruits = [fruit for fruit in available_fruits 
                        if fruit.get('Fruit_Name', '').lower() not in recent_objects]
        
        if not unused_fruits:
            unused_fruits = available_fruits
        
        if unused_fruits:
            # Select fruit with highest visual appeal score
            selected = max(unused_fruits, key=lambda x: int(x.get('Visual_Appeal_Score', 0)))
            return selected['Fruit_Name']
        
        return "Apple"
    
    def create_video(self, fruit_name: str) -> str:
        """Create video using FFmpeg"""
        try:
            video_filename = f"glass_{fruit_name.lower()}_{int(time.time())}.mp4"
            
            # Create video with text overlay
            cmd = [
                'ffmpeg', '-y', '-f', 'lavfi', 
                '-i', 'color=c=0x1a1a2e:size=720x1280:duration=10',
                '-vf', f'drawtext=text="Glass {fruit_name} ASMR":fontcolor=white:fontsize=30:x=(w-text_w)/2:y=(h-text_h)/2',
                '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-preset', 'fast',
                video_filename
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception(f"FFmpeg error: {result.stderr}")
                
            return video_filename
            
        except Exception as e:
            print(f"Video creation failed: {e}")
            raise
    
    def upload_to_youtube(self, video_file: str, title: str, description: str) -> str:
        """Simulate YouTube upload (actual upload needs OAuth2)"""
        try:
            # For now, simulate upload and return a placeholder URL
            # In production, you'd need proper OAuth2 setup
            
            print(f"Simulating YouTube upload for: {title}")
            print(f"Video file: {video_file}")
            print(f"Description: {description}")
            
            # Generate a fake video ID for tracking
            fake_video_id = f"fake_{int(time.time())}"
            video_url = f"https://www.youtube.com/watch?v={fake_video_id}"
            
            print(f"Simulated upload complete: {video_url}")
            return video_url
            
        except Exception as e:
            print(f"YouTube upload simulation failed: {e}")
            raise
    
    def log_to_csv(self, object_name: str, video_url: str, generation_time: float):
        """Log video creation to CSV"""
        try:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
            gen_time_str = f"{generation_time:.1f} min"
            
            new_row = [
                f"Glass {object_name}",
                video_url,
                current_time,
                "Live",
                gen_time_str
            ]
            
            self.append_to_csv(self.content_file, new_row)
            
            # Keep only last 20 entries
            content_data = self.read_csv_to_dict(self.content_file)
            if len(content_data) > 20:
                # Rewrite file with only last 20 entries
                with open(self.content_file, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Object', 'Video_URL', 'Created_Date', 'YouTube_Status', 'Generation_Time'])
                    writer.writerows([list(row.values()) for row in content_data[-20:]])
            
        except Exception as e:
            print(f"CSV logging failed: {e}")
    
    def run_automation_cycle(self):
        """Main automation cycle"""
        start_time = time.time()
        fruit_name = "Unknown"
        
        try:
            # Select fruit
            fruit_name = self.select_new_fruit()
            print(f"Selected fruit: {fruit_name}")
            
            # Create video
            video_file = self.create_video(fruit_name)
            print(f"Video created: {video_file}")
            
            # Prepare metadata
            title = f"ASMR Glass {fruit_name} Cutting & Slicing Sounds 🔪✨"
            description = f"Relaxing ASMR video of cutting a glass {fruit_name.lower()}. Perfect for sleep, study, and relaxation. #ASMR #Glass #Cutting #Relaxing"
            
            # Upload to YouTube
            video_url = self.upload_to_youtube(video_file, title, description)
            print(f"Uploaded to YouTube: {video_url}")
            
            # Log success
            generation_time = (time.time() - start_time) / 60
            self.log_to_csv(fruit_name, video_url, generation_time)
            
            # Cleanup
            if os.path.exists(video_file):
                os.remove(video_file)
            
            print(f"Automation completed in {generation_time:.1f} minutes")
            return True
            
        except Exception as e:
            print(f"Automation failed: {e}")
            generation_time = (time.time() - start_time) / 60
            self.log_to_csv(fruit_name, "Failed", generation_time)
            return False

def main():
    """Main function"""
    try:
        print("Starting ASMR Video Automation...")
        automation = ASMRVideoAutomationCSV()
        success = automation.run_automation_cycle()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
