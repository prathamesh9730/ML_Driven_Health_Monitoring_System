# health_bot.py
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from flask import Flask, request, jsonify
from threading import Thread
from datetime import datetime
import asyncio
import sheet_handler  # make sure this has log_prediction()

# ---------------- Constants ----------------
BOT_TOKEN = "7454526195:AAGoDbFnPkQQG8g3oJQ5w4Cn071ZtyrxbmE"  # replace with your bot token
ASK_NAME, ASK_CONTACT = range(2)

# ---------------- Global user info ----------------
# Supports multiple users: key = chat_id, value = {name, contact}
registered_users = {}

# ---------------- Flask App ----------------
app = Flask(__name__)
app_bot = Application.builder().token(BOT_TOKEN).build()

# ---------------- Telegram Handlers ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome to AI-Driven Health Monitoring System 🚑")
    await update.message.reply_text("Please enter your name (alphabets only):")
    return ASK_NAME

async def ask_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text.strip()
    if not name.isalpha():
        await update.message.reply_text("❌ Invalid name. Enter alphabets only.")
        return ASK_NAME
    context.user_data['name'] = name
    await update.message.reply_text("✅ Name saved! Now enter your 10-digit contact number:")
    return ASK_CONTACT

async def ask_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.text.strip()
    if not (contact.isdigit() and len(contact) == 10):
        await update.message.reply_text("❌ Invalid contact number. Enter 10 digits:")
        return ASK_CONTACT

    chat_id = update.effective_chat.id
    registered_users[chat_id] = {
        'name': context.user_data['name'],
        'contact': contact
    }

    await update.message.reply_text(
        f"✅ Details saved!\n👤 Name: {registered_users[chat_id]['name']}\n"
        f"📞 Contact: {registered_users[chat_id]['contact']}"
    )
    return ConversationHandler.END

# ---------------- Async Telegram Sender ----------------
async def send_telegram(chat_id, message):
    try:
        await app_bot.bot.send_message(chat_id=chat_id, text=message)
        print(f"💬 Sent to Telegram (chat_id={chat_id}): {message}")
    except Exception as e:
        print(f"❌ Telegram send failed: {e}")

# ---------------- Flask API ----------------
@app.route("/predict", methods=["POST"])
def predict():
    """
    Expects JSON:
    {
        "chat_id": <telegram_chat_id>,
        "values": [HR, SpO2, Temp],
        "status": "Normal/Warning/Critical"
    }
    """
    data = request.json
    chat_id = data.get("chat_id")
    values = data.get("values")  # [HR, SpO2, Temp]
    status = data.get("status")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if chat_id in registered_users:
        user_info = registered_users[chat_id]
        # Log to Google Sheets
        sheet_handler.log_prediction(
            name=user_info.get('name', 'Unknown'),
            contact=user_info.get('contact', '0000000000'),
            values=values,
            status=status
        )

        # Send Telegram message asynchronously
        message = (
            f"📟 Sensor Data -> HR:{values[0]} | SpO2:{values[1]} | Temp:{values[2]}\n"
            f"🤖 Status: {status}\n⏰ Time: {timestamp}"
        )
        # Schedule async task
        asyncio.run_coroutine_threadsafe(send_telegram(chat_id, message), app_bot.bot.loop)

    else:
        print(f"⚠️ Chat ID {chat_id} not registered. User must /start first.")

    return jsonify({"status": "success", "message": "Prediction sent!"})

# ---------------- Run Telegram Bot ----------------
def run_telegram_bot():
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_name)],
            ASK_CONTACT: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_contact)],
        },
        fallbacks=[],
    )
    app_bot.add_handler(conv_handler)
    print("🤖 Telegram Bot started in background thread...")
    app_bot.run_polling()

# ---------------- Main ----------------
def main():
    # Start Telegram bot in a separate thread
    Thread(target=run_telegram_bot, daemon=True).start()
    print("🌐 Flask API running on main thread...")
    app.run(debug=True, use_reloader=False)

if __name__ == "__main__":
    main()
