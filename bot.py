import requests
import time

TOKEN = "8363573696:AAGXpD4T4OuNu93Z98OrTL8G3z6KM-vDsxY"
CHAT_ID = "-1002013620572"

print("BOT STARTED SUCCESSFULLY")

# Emojis you want (edit here)
EMOJIS = ["🤣","🤣","🤣","🤣","🤣","😭","😭","😭","❤️","❤️"]

last_update_id = None

def react(message_id, emoji):
    url = f"https://api.telegram.org/bot{TOKEN}/setMessageReaction"
    payload = {
        "chat_id": CHAT_ID,
        "message_id": message_id,
        "reaction": [{"type": "emoji", "emoji": emoji}]
    }
    requests.post(url, json=payload)

while True:
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    r = requests.get(url).json()

    if r["result"]:
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

                for emoji in EMOJIS:
                    react(message_id, emoji)
                    time.sleep(0.4)  # avoid TELEGRAM LIMIT

    time.sleep(2)
