🤖 **Enterprise-Grade HR Management Bot with AI-Powered Features**

![Version](https://img.shields.io/badge/version-5.0-blue)
![Python](https://img.shields.io/badge/python-3.11+-green)
![License](https://img.shields.io/badge/license-Proprietary-red)

## ✨ Features

### Core HR Modules
- 📍 **Smart Attendance** - Clock in/out with automatic tracking
- 💰 **Payroll Management** - Salary slips, history, insights
- 🏖️ **Leave Management** - Request, track, balance monitoring
- ⏰ **Overtime Tracking** - Hours & compensation calculation

### Advanced Features
- 🤖 **AI Assistant** - Natural language HR queries (GROQ-powered)
- 🎮 **Gamification** - Points, levels (Bronze→Diamond), achievements
- 📊 **Performance Analytics** - 360° scoring, KPIs, feedback
- 📈 **Career Path** - Growth timeline, readiness score

### Power Tools
- 💳 **Expense Tracker** - Submit & track reimbursements
- 🤝 **Team Collaboration** - Projects, tasks, documents
- 📚 **Learning Hub** - Courses, certifications, progress
- 🏃 **Wellness Center** - Health tracking, programs
- 📄 **Document Vault** - Secure encrypted storage
- 🎯 **Goal Tracker** - Objectives & KPIs monitoring

## 🚀 Quick Start

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

## 🔐 Environment Variables

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

## 📦 Dependencies
```
python-telegram-bot==21.0.1
python-dotenv==1.0.0
sqlalchemy==2.0.25
langchain + GROQ integration
chromadb==0.4.22
And more...
```

See `requirements.txt` for complete list.

## 🌐 Deployment

### Railway (Recommended - Free Tier Available)

1. Push code to GitHub
2. Go to [railway.app](https://railway.app)
3. New Project → Deploy from GitHub
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

## 📁 Project Structure
```
BPKH-HR-Chatbot/
├── bot.py                 # Main bot application
├── config/
│   ├── settings.py       # Configuration management
│   └── settings.example.py
├── models/               # Database models
│   ├── __init__.py
│   └── models.py
├── handlers/             # Command handlers
├── utils/               # Utilities
│   └── advanced_rag.py  # AI/RAG engine
├── .env.example         # Environment template
├── .gitignore          # Git ignore rules
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🎯 Usage

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

## 👨‍💻 Developer

**MS Hadianto**
- 📧 Email: mshadianto@outlook.com
- 🐙 GitHub: [@mshadianto](https://github.com/mshadianto)
- 💼 LinkedIn: [MS Hadianto](https://linkedin.com/in/mshadianto)

## 🔒 Security

- ✅ Environment variables for secrets
- ✅ GitHub secret scanning enabled
- ✅ API key rotation supported
- ✅ Encrypted database connections
- ❌ Never commit `.env` file

## 📄 License

**Proprietary** - BPKH Internal Use Only

Unauthorized copying, distribution, or use is strictly prohibited.

## 🆘 Support

For issues or questions:
- 📧 Email: mshadianto@outlook.com
- 🐛 GitHub Issues: [Report Issue](https://github.com/mshadianto/BPKH-HR-Chatbot/issues)

## 🙏 Acknowledgments

Built with:
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- [LangChain](https://github.com/langchain-ai/langchain)
- [GROQ](https://groq.com)
- [SQLAlchemy](https://www.sqlalchemy.org/)

---

**Made with ❤️ for BPKH**

*Enterprise HR Management Made Simple*
EOF
