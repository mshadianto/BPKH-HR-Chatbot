import os
from pathlib import Path
BASE_DIR = Path(__file__).parent.parent
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'YOUR_OPENAI_KEY_HERE')
DATABASE_URL = f'sqlite:///{BASE_DIR}/data/hr_bot.db'
ADMIN_USER_IDS = [123456789]
