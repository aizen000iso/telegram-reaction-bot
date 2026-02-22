import requests
import time
import random

# 🔐 Your 6 bot tokens (NO empty ones)
TOKENS = [
    "8363573696:AAGXpD4T4OuNu93Z98OrTL8G3z6KM-vDsxY",  
    "8578327028:AAHdKRpxMXstzhNssPWEhkkDN9Ikdl4GPxM",  
    "8208309317:AAECJbrof5vzmhhA6OAV5y6qPFelNDRG-CA", 
    "8533257258:AAGfs9YqHEKcpi_IudzO9R7y8d_xWUlGlvM",  
    "8323392358:AAH371x6ZqiN9ZTjFPNxyisJbrc9nBped7E",  
    "8565508773:AAEHfm-wrKmxh7b9Cc88KsQFBClZNnX4NX4",
]

CHAT_ID = "-1002013620572"

print("SMART REACTION BOT STARTED")

last_update_id = None

# Pool for the 3 random reactions
RANDOM_POOL = ["❤️", "😭", "🙏", "🔥", "👍", "⚡", "👀", "💯"]


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


def build_reaction_pattern():
    """
    Always:
    3 🤣 + 3 random emojis
    Then shuffle so order looks natural.
    """
    reactions = ["🤣", "🤣", "🤣"]

    # pick 3 random unique emojis
    reactions += random.sample(RANDOM_POOL, 3)

    # shuffle order so bots don't look patterned
    random.shuffle(reactions)

    return reactions


def react_all(message_id):
    emojis = build_reaction_pattern()

    for token, emoji in zip(TOKENS, emojis):
        time.sleep(random.uniform(1.5, 2.4))  # human-like delay
        react(token, message_id, emoji)


while True:
    try:
        # ✅ Use offset so old posts are NEVER processed again
        url = f"https://api.telegram.org/bot{TOKENS[0]}/getUpdates"

        params = {}
        if last_update_id is not None:
            params["offset"] = last_update_id + 1

        response = requests.get(url, params=params, timeout=20).json()

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
                print("New post detected →", message_id)

                react_all(message_id)

        time.sleep(2)

    except Exception as e:
        print("Main loop error:", e)
        time.sleep(5)
