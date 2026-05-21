from flask import Flask, request
import asyncio
import zalo_bot

app = Flask(__name__)

BOT_TOKEN = "TOKEN"

CHAT_IDS = [
    "0a60ffd8fd9a14c44d8b",
    "bacc1925f26e1b30427f",
    "0f848926606b8935d07a"
]

async def send_zalo(msg):

    bot = zalo_bot.Bot(BOT_TOKEN)

    async with bot:

        for chat_id in CHAT_IDS:

            try:
                await bot.send_message(chat_id, msg)
            except Exception as e:
                print(e)

@app.route("/", methods=["GET"])
def home():
    return "OK"

@app.route("/alert", methods=["POST"])
def alert():

    data = request.json

    print(data)

    status = data.get("alertTypeFriendlyName", "UNKNOWN")

    if status == "Down":

        asyncio.run(
            send_zalo(
                "⚠️ Server lỏ rồi!"
            )
        )

    elif status == "Up":

        asyncio.run(
            send_zalo(
                "🟢 Server ONLINE!"
            )
        )

    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)