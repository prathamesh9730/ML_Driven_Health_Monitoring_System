import serial
import time
from health import predict_status
from datetime import datetime
import requests

# Flask API URL from merged health_bot.py
FLASK_API_URL = "http://127.0.0.1:5000/predict"

# Thresholds for realistic readings
MIN_HR = 30
MAX_HR = 220

def main():
    try:
        ser = serial.Serial('COM4', 115200, timeout=2)
        time.sleep(2)
        print(f"✅ Connected to serial port: {ser.port}")
    except Exception as e:
        print("❌ Failed to connect to serial port:", e)
        return

    while True:
        try:
            line = ser.readline().decode(errors="ignore").strip()

            # Skip empty lines or "No Finger Detected"
            if not line or "No Finger Detected" in line:
                print("⚠️ No Finger Detected - Skipping record...")
                continue

            # Try to parse HR, SpO2, Temp
            try:
                hr_str = line.split("HR:")[1].split(",")[0].strip()
                spo2_str = line.split("SpO2:")[1].split(",")[0].strip()
                temp_str = line.split("Temp:")[1].split(",")[0].strip()

                heart_rate = float(hr_str)
                spo2 = float(spo2_str)
                temp = float(temp_str)

            except (IndexError, ValueError) as e:
                print(f"⚠️ Could not parse line: '{line}' | Error: {e}")
                continue

            # Filter unrealistic HR readings
            if heart_rate < MIN_HR or heart_rate > MAX_HR:
                print(f"⚠️ Ignored unrealistic HR: {heart_rate} | SpO2: {spo2} | Temp: {temp}")
                continue

            values = [heart_rate, spo2, temp]

            # Debug info: show raw sensor values
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"📟 {timestamp} -> HR: {heart_rate} | SpO2: {spo2} | Temp: {temp}")

            # Prediction using health.py
            status = predict_status(values)
            print(f"🩺 {timestamp} -> Predicted Status: {status}")

            # Send to Flask API for Sheets + Telegram
            try:
                response = requests.post(FLASK_API_URL, json={"values": values, "status": status})
                if response.status_code == 200:
                    print("✅ Sent to Flask API successfully")
                else:
                    print(f"❌ Flask API Error {response.status_code}: {response.text}")
            except Exception as e:
                print(f"❌ Failed to send to Flask API: {e}")

        except Exception as e:
            print("❌ Error in main loop:", e)

if __name__ == "__main__":
    main()
