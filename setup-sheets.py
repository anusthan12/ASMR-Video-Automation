#!/usr/bin/env python3
"""
Setup script to initialize Google Sheets for ASMR automation
Run this once to set up your sheets with the proper structure and sample data
"""

import gspread
from google.oauth2.service_account import Credentials
import json
import os

def setup_google_sheets():
    """Initialize Google Sheets with proper structure"""
    
    # Setup credentials
    google_creds_json = os.getenv('GOOGLE_CREDENTIALS_JSON')
    if not google_creds_json:
        print("❌ GOOGLE_CREDENTIALS_JSON environment variable not set")
        return
    
    import base64
    creds_data = json.loads(base64.b64decode(google_creds_json).decode())
    creds = Credentials.from_service_account_info(
        creds_data,
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    
    gc = gspread.authorize(creds)
    
    # Open or create the spreadsheet
    sheet_id = os.getenv('GOOGLE_SHEET_ID', '1zKWr1zeoadgbJTd7E24N2TBXJKHlnQS9GW5I0-_9IgA')
    
    try:
        spreadsheet = gc.open_by_key(sheet_id)
        print(f"✅ Opened existing spreadsheet: {spreadsheet.title}")
    except:
        print("❌ Could not open spreadsheet. Please ensure:")
        print("1. The sheet exists and is shared with your service account")
        print("2. The GOOGLE_SHEET_ID is correct")
        return
    
    # Setup ASMR Content Tracker sheet
    setup_content_tracker(spreadsheet)
    
    # Setup Fruit Database sheet
    setup_fruit_database(spreadsheet)
    
    # Setup Settings sheet
    setup_settings(spreadsheet)
    
    print("✅ All sheets configured successfully!")

def setup_content_tracker(spreadsheet):
    """Setup the ASMR Content Tracker sheet"""
    try:
        worksheet = spreadsheet.worksheet('ASMR Content Tracker')
        print("✅ Found existing 'ASMR Content Tracker' sheet")
    except:
        worksheet = spreadsheet.add_worksheet(title='ASMR Content Tracker', rows=100, cols=7)
        print("✅ Created 'ASMR Content Tracker' sheet")
    
    # Set headers
    headers = [
        'Object', 'Video_URL', 'Created_Date', 'YouTube_Status', 
        'Instagram_Status', 'TikTok_Status', 'Generation_Time'
    ]
    worksheet.update('A1:G1', [headers])
    
    # Add sample data if sheet is empty
    if len(worksheet.get_all_values()) == 1:  # Only headers
        sample_data = [
            ['Glass Apple', 'https://example.com/video1', '2025-01-15', 'Live', 'Live', 'Live', '5.2 min'],
            ['Glass Orange', 'https://example.com/video2', '2025-01-14', 'Live', 'Live', 'Live', '4.8 min'],
            ['Glass Strawberry', 'https://example.com/video3', '2025-01-13', 'Live', 'Pending', 'Live', '6.1 min']
        ]
        worksheet.update('A2:G4', sample_data)
        print("✅ Added sample data to Content Tracker")

def setup_fruit_database(spreadsheet):
    """Setup the Fruit Database sheet"""
    try:
        worksheet = spreadsheet.worksheet('Fruit_Database')
        print("✅ Found existing 'Fruit_Database' sheet")
    except:
        worksheet = spreadsheet.add_worksheet(title='Fruit_Database', rows=100, cols=3)
        print("✅ Created 'Fruit_Database' sheet")
    
    # Set headers
    headers = ['Fruit_Name', 'Category', 'Visual_Appeal_Score']
    worksheet.update('A1:C1', [headers])
    
    # Add comprehensive fruit database if sheet is empty
    if len(worksheet.get_all_values()) == 1:  # Only headers
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
            ['Coconut', 'Tropical', '6'],
            ['Papaya', 'Tropical', '7'],
            ['Dragon Fruit', 'Exotic', '10'],
            ['Passion Fruit', 'Exotic', '8'],
            ['Pomegranate', 'Exotic', '9'],
            ['Fig', 'Exotic', '7'],
            ['Avocado', 'Tropical', '6'],
            ['Blueberry', 'Berry', '8'],
            ['Blackberry', 'Berry', '8'],
            ['Raspberry', 'Berry', '9'],
            ['Cranberry', 'Berry', '7'],
            ['Apricot', 'Stone', '8'],
            ['Nectarine', 'Stone', '9'],
            ['Persimmon', 'Exotic', '8'],
            ['Lychee', 'Exotic', '9'],
            ['Rambutan', 'Exotic', '8'],
            ['Starfruit', 'Exotic', '9'],
            ['Guava', 'Tropical', '7'],
            ['Pomelo', 'Citrus', '6'],
            ['Tangerine', 'Citrus', '8'],
            ['Mandarin', 'Citrus', '8'],
            ['Grapefruit', 'Citrus', '7'],
            ['Cantaloupe', 'Melon', '7'],
            ['Honeydew', 'Melon', '7']
        ]
        worksheet.update('A2:C40', fruit_data)
        print("✅ Added fruit database with 39 fruits")

def setup_settings(spreadsheet):
    """Setup the Settings sheet"""
    try:
        worksheet = spreadsheet.worksheet('Settings')
        print("✅ Found existing 'Settings' sheet")
    except:
        worksheet = spreadsheet.add_worksheet(title='Settings', rows=20, cols=3)
        print("✅ Created 'Settings' sheet")
    
    # Set headers
    headers = ['Setting', 'Value', 'Description']
    worksheet.update('A1:C1', [headers])
    
    # Add settings if sheet is empty
    if len(worksheet.get_all_values()) == 1:  # Only headers
        settings_data = [
            ['Schedule_Hours', '8', 'Hours between automated runs'],
            ['Max_Recent_Objects', '7', 'Number of recent objects to avoid'],
            ['Video_Duration_Seconds', '60', 'Target video duration'],
            ['Max_Retries', '3', 'Max retries on failure'],
            ['Upload_To_YouTube', 'true', 'Enable YouTube uploads'],
            ['Upload_To_Instagram', 'false', 'Enable Instagram uploads (requires setup)'],
            ['Upload_To_TikTok', 'false', 'Enable TikTok uploads (requires setup)'],
            ['Log_Level', 'INFO', 'Logging level (DEBUG, INFO, WARNING, ERROR)'],
            ['Cleanup_Days', '30', 'Days to keep old entries in sheet'],
            ['Enable_Notifications', 'false', 'Send email notifications on completion']
        ]
        worksheet.update('A2:C11', settings_data)
        print("✅ Added default settings")

if __name__ == "__main__":
    setup_google_sheets()
