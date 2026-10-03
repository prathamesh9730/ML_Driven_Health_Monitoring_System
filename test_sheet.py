# test_sheet.py
from sheet_handler import log_prediction

# ---------------- Test Data ----------------
test_name = "Prathamesh"
test_contact = "9876543210"
test_values = [120,98,36.5]  # HR, SpO2, Temp
test_status = "Normal"

# ---------------- Run Test ----------------
print("🚀 Testing Google Sheets Logging...")
log_prediction(test_name, test_contact, test_values, test_status)
print("✅ Test completed.")
