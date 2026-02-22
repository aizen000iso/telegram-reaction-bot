import requests
import time

# 🔐 PUT YOUR NEW TOKEN HERE (regenerate from BotFather if needed)
TOKEN = "YOUR_NEW_TOKEN_HERE"

# Your channel / group chat id (must start with -100 for channels)
CHAT_ID = "-1002013620572"

print("BOT STARTED SUCCESSFULLY")

# ✅ Keep only a few emojis — Telegram allows limited reactions per bot
EMOJIS = ["🤣", "😭", "❤️"]

last_update_id = None


def react_multiple(message_id):
    """
    Sends all reactions in ONE request (Telegram requirement)
    Includes delay to avoid spam detection.
    """

    # ⏱ Human-like delay (prevents Telegram anti-spam block)
    time.sleep(1.5)

    url = f"https://api.telegram.org/bot{TOKEN}/setMessageReaction"

    payload = {
        "chat_id": CHAT_ID,
        "message_id": message_id,
        "reaction": [{"type": "emoji", "emoji": e} for e in EMOJIS]
    }

    try:
        r = requests.post(url, json=payload, timeout=10)
        print("Reaction response:", r.text)
    except Exception as e:
        print("Reaction error:", e)


while True:
    try:
        # Get new updates
        url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
        r = requests.get(url, timeout=20).json()

        if r.get("result"):
            for update in r["result"]:
                if update["update_id"] != last_update_id:
                    last_update_id = update["update_id"]

                    # Works for both channel posts and group messages
                    if "channel_post" in update:
                        msg = update["channel_post"]
                    elif "message" in update:
                        msg = update["message"]
                    else:
                        continue

                    message_id = msg["message_id"]
                    print("New post detected →", message_id)

                    react_multiple(message_id)

        # Poll every 2 seconds (safe interval)
        time.sleep(2)

    except Exception as e:
        print("Main loop error:", e)
        time.sleep(5)
