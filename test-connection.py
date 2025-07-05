#!/usr/bin/env python3

import os
import json
import base64
import gspread
from google.oauth2.service_account import Credentials

def test_google_connection():
    print("🔍 Testing Google Sheets connection...")
    
    # Check environment variables
    sheet_id = os.getenv('GOOGLE_SHEET_ID')
    creds_json = os.getenv('GOOGLE_CREDENTIALS_JSON')
    
    if not sheet_id:
        print("❌ GOOGLE_SHEET_ID not set")
        return False
    
    if not creds_json:
        print("❌ GOOGLE_CREDENTIALS_JSON not set")
        return False
    
    print(f"📋 Sheet ID: {sheet_id}")
    print(f"🔑 Credentials length: {len(creds_json)}")
    
    try:
        # Decode credentials
        creds_data = json.loads(base64.b64decode(creds_json).decode())
        print(f"✅ Service account email: {creds_data.get('client_email', 'Not found')}")
        
        # Create credentials
        creds = Credentials.from_service_account_info(
            creds_data,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        
        # Test connection
        gc = gspread.authorize(creds)
        print("✅ Google Sheets client authorized")
        
        # Try to access the sheet
        try:
            sheet = gc.open_by_key(sheet_id)
            print(f"✅ Sheet found: {sheet.title}")
            print(f"📊 Sheet URL: {sheet.url}")
            
            # List worksheets
            worksheets = sheet.worksheets()
            print(f"📋 Worksheets found: {[ws.title for ws in worksheets]}")
            
            return True
            
        except gspread.SpreadsheetNotFound:
            print("❌ Spreadsheet not found!")
            print("📝 Creating a new spreadsheet...")
            
            # Create new spreadsheet
            new_sheet = gc.create(f"ASMR Automation Test")
            print(f"✅ Created new sheet: {new_sheet.title}")
            print(f"📋 New Sheet ID: {new_sheet.id}")
            print(f"📊 Sheet URL: {new_sheet.url}")
            print("⚠️  Update your GOOGLE_SHEET_ID secret with the new ID above")
            
            return True
            
        except Exception as e:
            print(f"❌ Error accessing sheet: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Credentials error: {e}")
        return False

if __name__ == "__main__":
    success = test_google_connection()
    exit(0 if success else 1)
