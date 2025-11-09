# BPKH HR Chatbot System

í´– **Enterprise-Grade HR Management Bot with AI-Powered Features**

![Version](https://img.shields.io/badge/version-5.0-blue)
![Python](https://img.shields.io/badge/python-3.11+-green)
![License](https://img.shields.io/badge/license-Proprietary-red)

## âœ¨ Features

### Core HR Modules
- í³ **Smart Attendance** - Clock in/out with automatic tracking
- í²° **Payroll Management** - Salary slips, history, insights
- í¿–ï¸ **Leave Management** - Request, track, balance monitoring
- â° **Overtime Tracking** - Hours & compensation calculation

### Advanced Features
- í´– **AI Assistant** - Natural language HR queries (GROQ-powered)
- í¾® **Gamification** - Points, levels (Bronzeâ†’Diamond), achievements
- í³Š **Performance Analytics** - 360Â° scoring, KPIs, feedback
- í³ˆ **Career Path** - Growth timeline, readiness score

### Power Tools
- í²³ **Expense Tracker** - Submit & track reimbursements
- ï¿½ï¿½ **Team Collaboration** - Projects, tasks, documents
- í³š **Learning Hub** - Courses, certifications, progress
- í¿ƒ **Wellness Center** - Health tracking, programs
- í³„ **Document Vault** - Secure encrypted storage
- í¾¯ **Goal Tracker** - Objectives & KPIs monitoring

## íº€ Quick Start

### Prerequisites
- Python 3.11+
- Telegram Bot Token
- GROQ API Key
- PostgreSQL/SQLite Database

### Installation
```bash
# 1. Clone repository
git clone https://github.com/mshadianto/BPKH-HR-Chatbot.git
cd BPKH-HR-Chatbot

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
nano .env  # Edit with your credentials

# 4. Run bot
python bot.py
```

## í´ Environment Variables

Create `.env` file with these variables:
```env
# Telegram Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_here

# GROQ AI Configuration
GROQ_API_KEY=your_groq_api_key_here

# Database Configuration
DATABASE_URL=postgresql://user:pass@host:port/db

# Logging
LOG_LEVEL=INFO
```

### Get Credentials:
- **Telegram Token**: [@BotFather](https://t.me/botfather)
- **GROQ API Key**: [console.groq.com](https://console.groq.com)

## í³¦ Dependencies
```
python-telegram-bot==21.0.1
python-dotenv==1.0.0
sqlalchemy==2.0.25
langchain + GROQ integration
chromadb==0.4.22
And more...
```

See `requirements.txt` for complete list.

## ï¿½ï¿½ Deployment

### Railway (Recommended - Free Tier Available)

1. Push code to GitHub
2. Go to [railway.app](https://railway.app)
3. New Project â†’ Deploy from GitHub
4. Select: `mshadianto/BPKH-HR-Chatbot`
5. Add environment variables in dashboard
6. Deploy!

### Manual VPS/Server
```bash
git clone https://github.com/mshadianto/BPKH-HR-Chatbot.git
cd BPKH-HR-Chatbot
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your credentials
python bot.py
```

Use systemd/supervisor for production.

## í³ Project Structure
```
BPKH-HR-Chatbot/
â”œâ”€â”€ bot.py                 # Main bot application
â”œâ”€â”€ config/
â”‚   â”œâ”€â”€ settings.py       # Configuration management
â”‚   â””â”€â”€ settings.example.py
â”œâ”€â”€ models/               # Database models
â”‚   â”œâ”€â”€ __init__.py
â”‚   â””â”€â”€ models.py
â”œâ”€â”€ handlers/             # Command handlers
â”œâ”€â”€ utils/               # Utilities
â”‚   â””â”€â”€ advanced_rag.py  # AI/RAG engine
â”œâ”€â”€ .env.example         # Environment template
â”œâ”€â”€ .gitignore          # Git ignore rules
â”œâ”€â”€ requirements.txt    # Python dependencies
â””â”€â”€ README.md          # This file
```

## í¾¯ Usage

### Start Bot
```
/start - Open main menu
/register - Register as employee
```

### Main Features
- **Attendance**: Clock in/out, view history
- **Payroll**: View slips, history, insights
- **Gamification**: Check level, leaderboard
- **AI Chat**: Ask HR questions naturally
- **Analytics**: Performance dashboard
- **Profile**: View employee information

## í±¨â€í²» Developer

**MS Hadianto**
- í³§ Email: mshadianto@outlook.com
- í°™ GitHub: [@mshadianto](https://github.com/mshadianto)
- í²¼ LinkedIn: [MS Hadianto](https://linkedin.com/in/mshadianto)

## í´’ Security

- âœ… Environment variables for secrets
- âœ… GitHub secret scanning enabled
- âœ… API key rotation supported
- âœ… Encrypted database connections
- âŒ Never commit `.env` file

## í³„ License

**Proprietary** - BPKH Internal Use Only

Unauthorized copying, distribution, or use is strictly prohibited.

## í¶˜ Support

For issues or questions:
- í³§ Email: mshadianto@outlook.com
- í°› GitHub Issues: [Report Issue](https://github.com/mshadianto/BPKH-HR-Chatbot/issues)

## í¹ Acknowledgments

Built with:
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- [LangChain](https://github.com/langchain-ai/langchain)
- [GROQ](https://groq.com)
- [SQLAlchemy](https://www.sqlalchemy.org/)

---

**Made with â¤ï¸ for BPKH**

*Enterprise HR Management Made Simple*
