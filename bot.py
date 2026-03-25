import requests
import time
import random
import threading

# 🔐 Your bot tokens
TOKENS = [
    "8363573696:AAGXpD4T4OuNu93Z98OrTL8G3z6KM-vDsxY",  
    "8578327028:AAHdKRpxMXstzhNssPWEhkkDN9Ikdl4GPxM",  
    "8208309317:AAECJbrof5vzmhhA6OAV5y6qPFelNDRG-CA", 
    "8533257258:AAGfs9YqHEKcpi_IudzO9R7y8d_xWUlGlvM",  
    "8323392358:AAH371x6ZqiN9ZTjFPNxyisJbrc9nBped7E",  
    "8565508773:AAEHfm-wrKmxh7b9Cc88KsQFBClZNnX4NX4",
    "8095952099:AAH_kZ0yXbGoDGRcUTwH73XNJFb8ZapqOkA",
    "8325442220:AAFd2NRCGTvZoPYFDKK9mYMZX-rjgaMAS1Y",
]

CHAT_ID = "-1002013620572"

print("🚀 HUMAN-LIKE REACTION BOT STARTED")

EMOJI_POOL = ["❤️", "😭", "🙏"]

last_update_id = None


def react(token, message_id, emoji, delay):
    """Send reaction after delay"""
    print(f"Bot waiting {delay}s before sending {emoji}")
    time.sleep(delay)

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
    reactions += random.choices(EMOJI_POOL, k=5)
    random.shuffle(reactions)
    return reactions


def react_parallel(message_id):
    emojis = build_pattern()
    threads = []

    for token, emoji in zip(TOKENS, emojis):
        delay = random.randint(60, 300)  # ⏱ 1–5 min random delay
        t = threading.Thread(target=react, args=(token, message_id, emoji, delay))
        t.start()
        threads.append(t)

    # Optional: wait for all threads (can remove if you want non-blocking)
    for t in threads:
        t.join()


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
                print("🔥 NEW POST DETECTED →", message_id)

                # Run reactions in parallel
                threading.Thread(target=react_parallel, args=(message_id,)).start()

        time.sleep(2)

    except Exception as e:
        print("Loop error:", e)
        time.sleep(5)
