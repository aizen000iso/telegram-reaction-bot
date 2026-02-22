import requests
import time

# 🔐 Put your REAL bot token here
TOKEN = "8363573696:AAGXpD4T4OuNu93Z98OrTL8G3z6KM-vDsxY"

# Your channel ID (must start with -100)
CHAT_ID = "-1002013620572"

print("BOT STARTED SUCCESSFULLY")

last_update_id = None


def react_single(message_id):
    """
    React to a message with ONE emoji (Telegram-safe).
    """

    # Small delay so Telegram doesn't flag as spam
    time.sleep(1.5)

    url = f"https://api.telegram.org/bot{TOKEN}/setMessageReaction"

    payload = {
        "chat_id": CHAT_ID,
        "message_id": message_id,
        "reaction": [
            {
                "type": "emoji",
                "emoji": "🤣"
            }
        ]
    }

    try:
        r = requests.post(url, json=payload, timeout=10)
        print("Reaction response:", r.text)
    except Exception as e:
        print("Reaction error:", e)


while True:
    try:
        # Get new updates from Telegram
        url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
        response = requests.get(url, timeout=20).json()

        if response.get("result"):
            for update in response["result"]:
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

                    react_single(message_id)

        # Check every 2 seconds
        time.sleep(2)

    except Exception as e:
        print("Main loop error:", e)
        time.sleep(5)
