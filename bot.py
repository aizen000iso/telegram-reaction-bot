import requests
import time

# 🔐 ADD YOUR 6 BOT TOKENS HERE
TOKENS = [
    "8363573696:AAGXpD4T4OuNu93Z98OrTL8G3z6KM-vDsxY",  
    "8578327028:AAHdKRpxMXstzhNssPWEhkkDN9Ikdl4GPxM",  
    "8208309317:AAECJbrof5vzmhhA6OAV5y6qPFelNDRG-CA", 
    "8533257258:AAGfs9YqHEKcpi_IudzO9R7y8d_xWUlGlvM",  
    "8323392358:AAH371x6ZqiN9ZTjFPNxyisJbrc9nBped7E",  
    "8565508773:AAEHfm-wrKmxh7b9Cc88KsQFBClZNnX4NX4",
]

CHAT_ID = "-1002013620572"

print("6-REACTION BOT STARTED")

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


def react_all(message_id):
    """
    Desired reaction result:
    🤣 🤣 🤣 🤣 😭 🙏
    """

    emojis = ["🤣", "🤣", "🤣", "🤣", "😭", "🙏"]

    for token, emoji in zip(TOKENS, emojis):
        time.sleep(2)  # IMPORTANT anti-spam delay
        react(token, message_id, emoji)


while True:
    try:
        # Only first bot listens for updates
        url = f"https://api.telegram.org/bot{TOKENS[0]}/getUpdates"
        response = requests.get(url, timeout=20).json()

        if response.get("result"):
            for update in response["result"]:
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

                    react_all(message_id)

        time.sleep(2)

    except Exception as e:
        print("Main loop error:", e)
        time.sleep(5)
