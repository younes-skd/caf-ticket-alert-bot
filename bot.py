import requests
import time
import telegram
from bs4 import BeautifulSoup

BOT_TOKEN = "8523628658:AAF3n8ZQQxAT8N4_MinX-8AewXpMB8Z0zeo"
CHAT_ID = None   # Will be auto-filled on first message

URL = "https://tickets.cafonline.com/fr"
CHECK_INTERVAL = 120  # seconds

bot = telegram.Bot(token=BOT_TOKEN)

def check_tickets():
    try:
        response = requests.get(URL, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # Detect the presence of “Acheter” button or similar wording
        keywords = ["Acheter", "Buy", "Billets", "Tickets"]

        text = soup.get_text().lower()
        return any(word.lower() in text for word in keywords)

    except Exception as e:
        print("Error checking page:", e)
        return False

print("Bot started. Waiting for your /start message...")

# Wait for user to send /start to collect chat ID
while CHAT_ID is None:
    updates = bot.get_updates()
    for u in updates:
        if u.message and u.message.text == "/start":
            CHAT_ID = u.message.chat.id
            bot.send_message(chat_id=CHAT_ID, text="Ticket alert activated! I’ll notify you instantly when tickets are available.")
            print("CHAT_ID set to:", CHAT_ID)
    time.sleep(1)

# Main loop
while True:
    available = check_tickets()
    if available:
        bot.send_message(chat_id=CHAT_ID, text="🔥🎟️ Tickets are AVAILABLE! Hurry!\n" + URL)
        time.sleep(3600)  # Avoid spam: wait 1 hour after alert
    time.sleep(CHECK_INTERVAL)
