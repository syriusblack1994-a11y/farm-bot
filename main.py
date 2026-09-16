async def show_vet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays the medical and vaccine list."""
    vet_text = (
        "🛡 *CRITICAL VACCINATION TIMELINE*\n\n"
        "• *Day 1:* Ensure calf drinks mother's *Og'iz suti* (Colostrum) immediately!\n"
        "• *Month 1:* Call vet for Anthrax (*Sibir yarasi*) vaccine.\n"
        "• *Month 3:* Foot-and-Mouth Disease (*Yashsil*) Shot #1.\n"
        "• *Month 6:* Deworming medicine (*Gijja dori*) before intensive stall feedlot starts.\n"
        "• *Month 9:* Foot-and-Mouth booster shot.\n\n"
        "⚠️ *Rule:* Always isolate any animal that stops eating and call your local tuman vet immediately."
    )
    await update.message.reply_text(vet_text, parse_mode="Markdown")

async def show_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Shows farm time metrics."""
    month = get_current_farm_month()
    status_text = (
        f"📅 *Farm Status Report*\n\n"
        f"• *Start Date:* October 1, 2026\n"
        f"• *Current Timeline:* Month {month} of the 36-Month Master Plan.\n"
        f"• *Target for this phase:* "
        f"{'Maximize milk sales and look after newborns.' if month <= 6 else 'Push heavy grain feed to bulls for rapid weight gain.'}"
    )
    await update.message.reply_text(status_text, parse_mode="Markdown")

# Automated Time Alerts Functions
async def morning_alert(context: ContextTypes.DEFAULT_TYPE) -> None:
    month = get_current_farm_month()
    text = "☀️ *MORNING FARM ALERT (06:00 AM)*\n\n" + generate_schedule_text(month)
    for chat_id in context.application.chat_data:
        await context.bot.send_message(chat_id=chat_id, text=text, parse_mode="Markdown")

async def noon_alert(context: ContextTypes.DEFAULT_TYPE) -> None:
    month = get_current_farm_month()
    text = "🌤 *NOON WATER & MINERAL CHECK (12:00 PM)*\n\n• Clean out water troughs completely.\n• Verify salt blocks are present."
    for chat_id in context.application.chat_data:
        await context.bot.send_message(chat_id=chat_id, text=text, parse_mode="Markdown")

async def evening_alert(context: ContextTypes.DEFAULT_TYPE) -> None:
    month = get_current_farm_month()
    text = "🌙 *EVENING ALERTS (16:00 / 18:00 PM)*\n\n" + generate_schedule_text(month)
    for chat_id in context.application.chat_data:
        await context.bot.send_message(chat_id=chat_id, text=text, parse_mode="Markdown")

def main() -> None:
    """Start the bot."""
    application = Application.builder().token(BOT_TOKEN).build()

    # Register text commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("schedule", show_schedule))
    application.add_handler(CommandHandler("vet", show_vet))
    application.add_handler(CommandHandler("status", show_status))

    # Schedule the recurring daily alerts
    job_queue = application.job_queue
    job_queue.run_daily(morning_alert, time=time(6, 0, 0))   # 06:00 AM daily
    job_queue.run_daily(noon_alert, time=time(12, 0, 0))     # 12:00 PM daily
    job_queue.run_daily(evening_alert, time=time(17, 0, 0))  # 05:00 PM daily

    # Run the bot until user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if name == "main":
    main()
