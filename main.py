import os
import asyncio
from datetime import date, datetime
from telegram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from flask import Flask

# ===== CONFIG =====
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Countdown window
START = date(2026,1,1)
END   = date(2026,1,22)

bot = Bot(token=BOT_TOKEN)

def get_days_remaining():
    today = datetime.utcnow().date()
    return (END - today).days

async def send_message():
    days_left = get_days_remaining()
    if 0 <= days_left <= 21:
        text = f"{days_left}- DAYS REMAIN :"
        await bot.send_message(chat_id=CHAT_ID, text=text)

# ==== FLASK KEEP-ALIVE ====
app = Flask(__name__)

@app.route("/")
def alive():
    return "Bot is alive!"

def run_flask():
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))

# ===== MAIN LOOP =====
async def main():
    # Start keep-alive server
    import threading
    threading.Thread(target=run_flask).start()

    scheduler = AsyncIOScheduler(timezone="UTC")
    scheduler.add_job(send_message, "cron", hour=1, minute=30)
    scheduler.start()

    while True:
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
