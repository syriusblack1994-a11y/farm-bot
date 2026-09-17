async def noon_alert(context: ContextTypes.DEFAULT_TYPE) -> None:
    subs = load_subscribers()
    for chat_id in subs:
        try:
            await context.bot.send_message(chat_id=chat_id, text="🌤 *MIDDAY CHECK (12:00 PM UZB)*\nClean water and check salt-lick block.", parse_mode="Markdown")
        except Exception as e:
            logging.error(f"Failed to send noon update to {chat_id}: {e}")

async def evening_alert(context: ContextTypes.DEFAULT_TYPE) -> None:
    subs = load_subscribers()
    for chat_id in subs:
        try:
            await context.bot.send_message(chat_id=chat_id, text="🌙 *EVENING FEEDING ALERT (17:00 PM UZB)*\nAdminister schedule routines.", parse_mode="Markdown")
        except Exception as e:
            logging.error(f"Failed to send evening update to {chat_id}: {e}")


def main() -> None:
    # Run dummy web server in a side thread so Render detects a port connection
    threading.Thread(target=run_health_server, daemon=True).start()

    # Build and trigger Telegram bot core polling loop
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("schedule", show_schedule))
    application.add_handler(CommandHandler("vet", show_vet))

    # Initialize Job Queue using explicitly targeted local times
    job_queue = application.job_queue
    if job_queue:
        job_queue.run_daily(morning_alert, time=time(6, 0, 0, tzinfo=UZB_TZ))
        job_queue.run_daily(noon_alert, time=time(12, 0, 0, tzinfo=UZB_TZ))
        job_queue.run_daily(evening_alert, time=time(17, 0, 0, tzinfo=UZB_TZ))
        logging.info("Job Queue successfully armed on Asia/Tashkent time.")
    else:
        logging.critical("Job Queue failed! Check dependencies.")

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if name == "main":
    main()
