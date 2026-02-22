import requests
import time
import random

TOKENS = [
    "8363573696:AAGXpD4T4OuNu93Z98OrTL8G3z6KM-vDsxY",  
    "8578327028:AAHdKRpxMXstzhNssPWEhkkDN9Ikdl4GPxM",  
    "8208309317:AAECJbrof5vzmhhA6OAV5y6qPFelNDRG-CA", 
    "8533257258:AAGfs9YqHEKcpi_IudzO9R7y8d_xWUlGlvM",  
    "8323392358:AAH371x6ZqiN9ZTjFPNxyisJbrc9nBped7E",  
    "8565508773:AAEHfm-wrKmxh7b9Cc88KsQFBClZNnX4NX4",
]

CHAT_ID = "-1002013620572"

print("LIVE REACTION BOT STARTED")

RANDOM_POOL = ["❤️", "😭", "🙏", "🔥", "👍", "⚡", "👀", "💯"]

last_update_id = None


def react(token, message_id, emoji):
    url = f"https://api.telegram.org/bot{token}/setMessageReaction"

    payload = {
        "chat_id": CHAT_ID,
        "message_id": message_id,
        "reaction": [{"type": "emoji", "emoji": emoji}]
    }

    try:
        r = requests.post(url, json=payload, timeout=10)
        print(f"{emoji} sent:", r.text)
    except Exception as e:
        print("Reaction error:", e)


def build_pattern():
    reactions = ["🤣", "🤣", "🤣"]
    reactions += random.sample(RANDOM_POOL, 3)
    random.shuffle(reactions)
    return reactions


def react_all(message_id):
    emojis = build_pattern()

    for token, emoji in zip(TOKENS, emojis):
        time.sleep(random.uniform(1.5, 2.4))
        react(token, message_id, emoji)


# ---- MAIN LOOP ----
while True:
    try:
        url = f"https://api.telegram.org/bot{TOKENS[0]}/getUpdates"

        params = {
            "timeout": 25,
            "offset": last_update_id + 1 if last_update_id else None
        }

        response = requests.get(url, params=params, timeout=30).json()

        if response.get("result"):
            for update in response["result"]:
                last_update_id = update["update_id"]

                if "channel_post" in update:
                    msg = update["channel_post"]
                elif "message" in update:
                    msg = update["message"]
                else:
                    continue

                message_id = msg["message_id"]
                print("NEW POST →", message_id)

                react_all(message_id)

        time.sleep(2)

    except Exception as e:
        print("Loop error:", e)
        time.sleep(5)
