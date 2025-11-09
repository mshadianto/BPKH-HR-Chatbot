#!/bin/bash
echo "íº€ Creating Telegram HR Bot..."
mkdir -p telegram_hr_bot/{config,models,handlers,utils,data,docs,scripts} && cd telegram_hr_bot
echo '"""Configuration package."""' > config/__init__.py
cat > config/settings.py << 'EOF'
import os
from pathlib import Path
BASE_DIR = Path(__file__).parent.parent
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'YOUR_OPENAI_KEY_HERE')
DATABASE_URL = f'sqlite:///{BASE_DIR}/data/hr_bot.db'
ADMIN_USER_IDS = [123456789]
EOF
echo '"""Package."""' > models/__init__.py
echo '"""Package."""' > handlers/__init__.py
echo '"""Package."""' > utils/__init__.py
cat > requirements.txt << 'EOF'
python-telegram-bot==20.7
sqlalchemy==2.0.23
langchain==0.1.0
openai==1.6.1
EOF
cat > bot.py << 'EOF'
import logging
from telegram import Update
from telegram.ext import Application
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
def main():
    logger.info("Bot template created!")
if __name__ == '__main__':
    main()
EOF
echo "âœ… Bot structure created! Run: pip install -r requirements.txt"
