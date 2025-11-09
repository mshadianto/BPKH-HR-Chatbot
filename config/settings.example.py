import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_TOKEN_HERE')
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./bpkh.db')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
