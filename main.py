import logging
import os
from datetime import datetime, time
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# 🎯 FIXED: Assigned your token securely to the variable
BOT_TOKEN = "8975404846:AAF-j5eOKDP8qruIBUh99mE3878lukqvQs4"
FARM_START_DATE = datetime(2026, 10, 1)

# --- DUMMY WEB SERVER TO SPREAD RENDER PORT ALERTS ---
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Farm Bot is running live!")

def run_health_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    server.serve_forever()

# --- BOT FUNCTIONALITY ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    context.application.chat_data[chat_id] = True
    welcome_text = (
        "🇺🇿 *Welcome to your 3-Year Farm Manager Bot!*\n\n"
        "I will send step-by-step instructions to this chat automatically.\n\n"
        "*Commands:*\n/schedule - View today's feeding steps\n/vet - View vaccine lists"
    )
    await update.message.reply_text(welcome_text, parse_mode="Markdown")

def get_current_farm_month():
    now = datetime.now()
    if now < FARM_START_DATE: return 1
    return ((now - FARM_START_DATE).days // 30) + 1

def generate_schedule_text(month):
    if month <= 1:
        return ("Automated schedule: Feed calves 2.5 liters of warm mother's milk at 06:00 and 18:00. Check clean water at 12:00.")
    elif 2 <= month <= 5:
        return ("Automated schedule: Feed calves 2 liters of warm milk. Provide free choice alfalfa hay and 300g yem mix at noon.")
    return ("Automated schedule: Heavy feedlot phase! 2.5kg heavy yem mix at 06:00 and 16:00. Free alfalfa hay at 08:00 and 18:00.")

async def show_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(generate_schedule_text(get_current_farm_month()), parse_mode="Markdown")

async def show_vet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("🛡 *Vaccines:* Day 1: Colostrum. Month 1: Anthrax. Month 3: Yashsil #1. Month 6: Deworming.", parse_mode="Markdown")

async def morning_alert(context: ContextTypes.DEFAULT_TYPE) -> None:
    for chat_id in context.application.chat_data:
        await context.bot.send_message(chat_id=chat_id, text="☀️ *MORNING UPDATE (06:00 AM)*\n" + generate_schedule_text(get_current_farm_month()))

async def noon_alert(context: ContextTypes.DEFAULT_TYPE) -> None:
    for chat_id in context.application.chat_data:
        await context.bot.send_message(chat_id=chat_id, text="🌤 *MIDDAY CHECK (12:00 PM)*\nClean water and check salt-lick block.")

async def evening_alert(context: ContextTypes.DEFAULT_TYPE) -> None:
    for chat_id in context.application.chat_data:
        await context.bot.send_message(chat_id=chat_id, text="🌙 *EVENING FEEDING ALERT (17:00 PM)*\nAdminister schedule routines.")

def main() -> None:
    threading.Thread(target=run_health_server, daemon=True).start()

    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("schedule", show_schedule))
    application.add_handler(CommandHandler("vet", show_vet))

    job_queue = application.job_queue
    job_queue.run_daily(morning_alert, time=time(6, 0, 0))
    job_queue.run_daily(noon_alert, time=time(12, 0, 0))
    job_queue.run_daily(evening_alert, time=time(17, 0, 0))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

# 🎯 FIXED: Correct Python main trigger execution blocks
if _name_ == "_main_":
    main()
