import threading
import health_bot
import serial_reader

def run_bot():
    try:
        health_bot.main()
    except Exception as e:
        print(f"❌ please check in Telegram Bot : {e}")

def run_serial_reader():
    try:
        serial_reader.main()
    except Exception as e:
        print(f"❌ please check in Serial Reader : {e}")

if __name__ == "__main__": 
    print("🚀 Starting AI-Driven Health Monitoring System...\n")

    # Thread for Telegram bot
    t1 = threading.Thread(target=run_bot, daemon=True)
    t1.start()

    # Thread for Serial Reader
    t2 = threading.Thread(target=run_serial_reader, daemon=True)
    t2.start()

    # Keep both running
    t1.join()
    t2.join()
