python
from flask import Flask, request
import asyncio
import zalo_bot
import time
from datetime import datetime

app = Flask(__name__)

# ===== CONFIG =====

BOT_TOKEN = "TOKEN"

CHAT_IDS = [
    "0a60ffd8fd9a14c44d8b",
    "bacc1925f26e1b30427f",
    "0f848926606b8935d07a"
]

# ==================


# ===== ZALO SEND =====

async def send_zalo(msg):

    bot = zalo_bot.Bot(BOT_TOKEN)

    async with bot:

        for chat_id in CHAT_IDS:

            try:
                await bot.send_message(chat_id, msg)

            except Exception as e:
                print(f"❌ ZALO ERROR: {e}")

# =====================


# ===== PING LOGGER =====

@app.before_request
def start_timer():

    request.start_time = time.time()


@app.after_request
def log_ping(response):

    if hasattr(request, "start_time"):

        duration = round(
            (time.time() - request.start_time) * 1000,
            2
        )

        now = datetime.now().strftime("%H:%M:%S")

        ip = request.remote_addr

        print(
            f"[{now}] 🚀 PING OK | "
            f"{request.method} {request.path} | "
            f"{duration}ms | IP: {ip}"
        )

    return response

# =========================


# ===== HOME =====

@app.route("/", methods=["GET"])
def home():

    return "OK"

# ==================


# ===== ALERT =====

@app.route("/alert", methods=["POST"])
def alert():

    try:

        data = request.json

        print(f"📩 ALERT DATA: {data}")

        status = data.get(
            "alertTypeFriendlyName",
            "UNKNOWN"
        )

        now = datetime.now().strftime("%H:%M:%S")

        # SERVER DOWN
        if status == "Down":

            print(f"[{now}] 🔴 SERVER DOWN!")

            asyncio.run(
                send_zalo(
                    "🔴 SERVER OFFLINE!\n\n"
                    "⚠️ Ping timeout hoặc server sập rồi ní!"
                )
            )

        # SERVER ONLINE
        elif status == "Up":

            print(f"[{now}] 🟢 SERVER ONLINE!")

            asyncio.run(
                send_zalo(
                    "🟢 SERVER ONLINE!\n\n"
                    "🚀 Server sống lại rồi ní!"
                )
            )

        return "ok"

    except Exception as e:

        print(f"❌ ALERT ERROR: {e}")

        return "error", 500

# ==================


# ===== START =====

if __name__ == "__main__":

    print("🚀 ZALO WEBHOOK SERVER STARTING...")

    app.run(
        host="0.0.0.0",
        port=5000
    )

# ==================

