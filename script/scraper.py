import os
import json
import logging
from datetime import datetime
from dotenv import load_dotenv
from telethon.sync import TelegramClient
from telethon.tl.types import MessageMediaPhoto

# Load API credentials
load_dotenv()
API_ID = int(os.getenv("api_id"))
API_HASH = os.getenv("api_hash")
PHONE = os.getenv("phone_number")

# Logging
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    filename=f"{log_dir}/scrape_{datetime.today().date()}.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Channel list
channels = {
    "chemed": "https://t.me/lobelia4cosmetics",
    "lobelia4cosmetics": "https://t.me/lobelia4cosmetics",
    "tikvahpharma": "https://t.me/tikvahpharma"
}

# Output directory
TODAY = datetime.today().strftime('%Y-%m-%d')
base_path = f"data/raw/telegram_messages/{TODAY}"
os.makedirs(base_path, exist_ok=True)
image_dir = f"{base_path}/images"
os.makedirs(image_dir, exist_ok=True)

# Connect to Telegram
client = TelegramClient("scraper_session", API_ID, API_HASH)

async def scrape_channel(name, link, limit=200):
    try:
        messages_data = []

        logging.info(f"Scraping channel: {name}")
        messages = await client.get_messages(link, limit=limit)

        for msg in messages:
            msg_dict = {
                "id": msg.id,
                "date": str(msg.date),
                "sender_id": msg.sender_id,
                "message": msg.text,
                "has_media": msg.media is not None
            }

            # Save image if exists
            if isinstance(msg.media, MessageMediaPhoto):
                image_path = f"{image_dir}/{name}_{msg.id}.jpg"
                await msg.download_media(file=image_path)
                msg_dict["image_path"] = image_path

            messages_data.append(msg_dict)

        # Save JSON
        with open(f"{base_path}/{name}.json", "w", encoding='utf-8') as f:
            json.dump(messages_data, f, ensure_ascii=False, indent=2)

        logging.info(f"Saved {len(messages_data)} messages from {name}")
    except Exception as e:
        logging.error(f"Error scraping {name}: {str(e)}")

with client:
    for name, link in channels.items():
        client.loop.run_until_complete(scrape_channel(name, link))
