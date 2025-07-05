#!/usr/bin/env python3

import os
import json
import base64
import time
import gspread
from google.oauth2.service_account import Credentials

def test_google_connection():
    print("Testing Google Sheets connection...")
    
    sheet_id = os.getenv('GOOGLE_SHEET_ID')
    creds_json = os.getenv('GOOGLE_CREDENTIALS_JSON')
    
    if not sheet_id:
        print("❌ GOOGLE_SHEET_ID not set")
        return False
    
    if not creds_json:
        print("❌ GOOGLE_CREDENTIALS_JSON not set")
        return False
    
    print(f"Sheet ID: {sheet_id}")
    
    try:
        creds_data = json.loads(base64.b64decode(creds_json).decode())
        print(f"Service account: {creds_data.get('client_email')}")
        print(f"Project ID: {creds_data.get('project_id')}")
        
        creds = Credentials.from_service_account_info(
            creds_data,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        
        gc = gspread.authorize(creds)
        print("✅ Google client authorized")
        
        # Try multiple times with backoff
        for attempt in range(3):
            try:
                sheet = gc.open_by_key(sheet_id)
                print(f"✅ Sheet found: {sheet.title}")
                print(f"✅ Sheet URL: {sheet.url}")
                
                # Test read access
                worksheets = sheet.worksheets()
                print(f"✅ Worksheets: {[ws.title for ws in worksheets]}")
                
                # Test write access
                test_ws = None
                try:
                    test_ws = sheet.worksheet('Test')
                except gspread.WorksheetNotFound:
                    test_ws = sheet.add_worksheet(title='Test', rows=10, cols=5)
                    print("✅ Created test worksheet")
                
                test_ws.update('A1', f'Test at {time.strftime("%Y-%m-%d %H:%M:%S")}')
                print("✅ Write test successful")
                
                # Clean up test
                sheet.del_worksheet(test_ws)
                print("✅ Test cleanup successful")
                
                return True
                
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt < 2:
                    print("Retrying in 5 seconds...")
                    time.sleep(5)
                else:
                    print("❌ All attempts failed")
                    return False
                    
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

if __name__ == "__main__":
    success = test_google_connection()
    exit(0 if success else 1)
