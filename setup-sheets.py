#!/usr/bin/env python3

import gspread
from google.oauth2.service_account import Credentials
import json
import os
import base64

def setup_google_sheets():
    google_creds_json = os.getenv('GOOGLE_CREDENTIALS_JSON')
    if not google_creds_json:
        print("❌ GOOGLE_CREDENTIALS_JSON environment variable not set")
        return
    
    creds_data = json.loads(base64.b64decode(google_creds_json).decode())
    creds = Credentials.from_service_account_info(
        creds_data,
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    
    gc = gspread.authorize(creds)
    sheet_id = os.getenv('GOOGLE_SHEET_ID')
    
    try:
        spreadsheet = gc.open_by_key(sheet_id)
        print(f"✅ Opened spreadsheet: {spreadsheet.title}")
    except:
        print("❌ Could not open spreadsheet")
        return
    
    setup_content_tracker(spreadsheet)
    setup_fruit_database(spreadsheet)
    setup_settings(spreadsheet)
    
    print("✅ All sheets configured successfully!")

def setup_content_tracker(spreadsheet):
    try:
        worksheet = spreadsheet.worksheet('ASMR Content Tracker')
        print("✅ Found existing 'ASMR Content Tracker' sheet")
    except:
        worksheet = spreadsheet.add_worksheet(title='ASMR Content Tracker', rows=100, cols=7)
        print("✅ Created 'ASMR Content Tracker' sheet")
    
    headers = [
        'Object', 'Video_URL', 'Created_Date', 'YouTube_Status', 
        'Instagram_Status', 'TikTok_Status', 'Generation_Time'
    ]
    worksheet.update('A1:G1', [headers])
    
    if len(worksheet.get_all_values()) == 1:
        sample_data = [
            ['Glass Apple', 'https://example.com/video1', '2025-01-15', 'Live', 'Live', 'Live', '5.2 min'],
            ['Glass Orange', 'https://example.com/video2', '2025-01-14', 'Live', 'Live', 'Live', '4.8 min']
        ]
        worksheet.update('A2:G3', sample_data)
        print("✅ Added sample data to Content Tracker")

def setup_fruit_database(spreadsheet):
    try:
        worksheet = spreadsheet.worksheet('Fruit_Database')
        print("✅ Found existing 'Fruit_Database' sheet")
    except:
        worksheet = spreadsheet.add_worksheet(title='Fruit_Database', rows=100, cols=3)
        print("✅ Created 'Fruit_Database' sheet")
    
    headers = ['Fruit_Name', 'Category', 'Visual_Appeal_Score']
    worksheet.update('A1:C1', [headers])
    
    if len(worksheet.get_all_values()) == 1:
        fruit_data = [
            ['Apple', 'Common', '9'],
            ['Orange', 'Citrus', '8'],
            ['Strawberry', 'Berry', '10'],
            ['Banana', 'Tropical', '7'],
            ['Grape', 'Berry', '9'],
            ['Kiwi', 'Exotic', '8'],
            ['Mango', 'Tropical', '10'],
            ['Pineapple', 'Tropical', '9'],
            ['Watermelon', 'Melon', '8'],
            ['Peach', 'Stone', '9'],
            ['Pear', 'Common', '8'],
            ['Cherry', 'Berry', '10'],
            ['Plum', 'Stone', '8'],
            ['Lemon', 'Citrus', '7'],
            ['Lime', 'Citrus', '7'],
            ['Dragon Fruit', 'Exotic', '10'],
            ['Passion Fruit', 'Exotic', '8'],
            ['Pomegranate', 'Exotic', '9'],
            ['Fig', 'Exotic', '7'],
            ['Blueberry', 'Berry', '8']
        ]
        worksheet.update('A2:C21', fruit_data)
        print("✅ Added fruit database")

def setup_settings(spreadsheet):
    try:
        worksheet = spreadsheet.worksheet('Settings')
        print("✅ Found existing 'Settings' sheet")
    except:
        worksheet = spreadsheet.add_worksheet(title='Settings', rows=20, cols=3)
        print("✅ Created 'Settings' sheet")
    
    headers = ['Setting', 'Value', 'Description']
    worksheet.update('A1:C1', [headers])
    
    if len(worksheet.get_all_values()) == 1:
        settings_data = [
            ['Schedule_Hours', '8', 'Hours between automated runs'],
            ['Max_Recent_Objects', '7', 'Number of recent objects to avoid'],
            ['Video_Duration_Seconds', '10', 'Target video duration'],
            ['Max_Retries', '3', 'Max retries on failure'],
            ['Upload_To_YouTube', 'true', 'Enable YouTube uploads']
        ]
        worksheet.update('A2:C6', settings_data)
        print("✅ Added default settings")

if __name__ == "__main__":
    setup_google_sheets()
