import logging
import os

from dotenv import load_dotenv
from telethon import TelegramClient

load_dotenv()

logging.basicConfig(format='[%(levelname)-8s%(asctime)s] %(message)s', level=logging.INFO)

API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
BOT_TOKEN = os.getenv('BOT_TOKEN')
POSTGRES_URI = os.getenv('POSTGRES_URI')
ADMIN = int(os.getenv('ADMIN'))
CHANNEL = int(os.getenv('CHANNEL'))
CHANNEL_URL = os.getenv('CHANNEL_URL')
GROUP = int(os.getenv('GROUP'))

client = TelegramClient('video-to-audio', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
