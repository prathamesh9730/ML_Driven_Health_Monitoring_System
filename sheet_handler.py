import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from threading import Lock
import time

# ---------------- Google Sheets Setup ----------------
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Replace with your spreadsheet key
SPREADSHEET_KEY = "1schTRZLJpJEVGVNc3_ig1rZWGtGDSCUz-LIXV-AQr3g"
sheet = client.open_by_key(SPREADSHEET_KEY).sheet1

# Lock to ensure thread-safe operations
sheet_lock = Lock()

# ---------------- Log Prediction ----------------
def log_prediction(name, contact, values, status, retries=3):
    """
    Append a new row to Google Sheet with sensor data and status.
    Thread-safe with retry on failure.
    """
    row = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        name,
        contact,
        values[0],  # HR
        values[1],  # SpO2
        values[2],  # Temp
        status
    ]

    for attempt in range(retries):
        try:
            with sheet_lock:
                sheet.append_row(row)
            print(f"✅ Logged to Google Sheet: {row}")
            return
        except Exception as e:
            print(f"❌ Attempt {attempt+1} failed to log to Google Sheet: {e}")
            time.sleep(2)  # wait before retry
    print("❌ Failed to log after multiple attempts.")
