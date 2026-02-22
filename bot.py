import requests
import time

TOKEN = "8363573696:AAGXpD4T4OuNu93Z98OrTL8G3z6KM-vDsxY"
CHAT_ID = "-1002013620572"

print("BOT STARTED SUCCESSFULLY")

# Telegram allows ONE reaction per emoji per bot → use UNIQUE emojis
EMOJIS = ["🤣", "😭", "❤️", "🔥", "👍", "🎉", "😍", "👀", "💯", "⚡"]

last_update_id = None


def react_multiple(message_id):
    url = f"https://api.telegram.org/bot{TOKEN}/setMessageReaction"

    payload = {
        "chat_id": CHAT_ID,
        "message_id": message_id,
        "reaction": [{"type": "emoji", "emoji": e} for e in EMOJIS],
        "is_big": False
    }

    r = requests.post(url, json=payload)
    print("Reaction response:", r.text)


while True:
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
        r = requests.get(url, timeout=20).json()

        if r.get("result"):
            for update in r["result"]:
                if update["update_id"] != last_update_id:
                    last_update_id = update["update_id"]

                    if "channel_post" in update:
                        msg = update["channel_post"]
                    elif "message" in update:
                        msg = update["message"]
                    else:
                        continue

                    message_id = msg["message_id"]
                    print("New post detected →", message_id)

                    react_multiple(message_id)

        time.sleep(2)

    except Exception as e:
        print("Error:", e)
        time.sleep(5)
