#!/bin/bash
# ============================================================================
# TELEGRAM BOT SDM - ONE-LINER SETUP SCRIPT FOR GIT BASH WINDOWS
# ============================================================================
# 
# QUICK START - Copy & paste ONE of these commands:
# 
# 1️⃣ BASIC SETUP (No dummy data):
# curl -sSL https://raw.githubusercontent.com/yourrepo/telegram-sdm-bot/main/setup.sh | bash
#
# 2️⃣ FULL SETUP (With 50 dummy employees):
# curl -sSL https://raw.githubusercontent.com/yourrepo/telegram-sdm-bot/main/setup.sh | bash -s -- --full
#
# 3️⃣ CUSTOM SETUP (Custom number of employees):
# curl -sSL https://raw.githubusercontent.com/yourrepo/telegram-sdm-bot/main/setup.sh | bash -s -- --employees 100
#
# OR MANUAL SETUP (if you already have the files):
# bash setup.sh --full
#
# ============================================================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
NUM_EMPLOYEES=50
FULL_SETUP=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --full)
            FULL_SETUP=true
            shift
            ;;
        --employees)
            NUM_EMPLOYEES="$2"
            FULL_SETUP=true
            shift 2
            ;;
        *)
            shift
            ;;
    esac
done

# Print banner
echo -e "${BLUE}"
echo "============================================================================"
echo "   🤖 TELEGRAM BOT SDM - AUTOMATED SETUP"
echo "============================================================================"
echo -e "${NC}"

# Check Python installation
echo -e "${YELLOW}[1/8]${NC} Checking Python installation..."
if ! command -v python &> /dev/null; then
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}❌ Python not found! Please install Python 3.9+${NC}"
        exit 1
    fi
    PYTHON_CMD="python3"
else
    PYTHON_CMD="python"
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✅ Found Python $PYTHON_VERSION${NC}"

# Check pip
echo -e "${YELLOW}[2/8]${NC} Checking pip..."
if ! $PYTHON_CMD -m pip --version &> /dev/null; then
    echo -e "${RED}❌ pip not found!${NC}"
    exit 1
fi
echo -e "${GREEN}✅ pip is available${NC}"

# Create project structure
echo -e "${YELLOW}[3/8]${NC} Creating project structure..."
mkdir -p {docs,scripts,configs,logs,data,backups,tests}
mkdir -p docs/{api,guides,screenshots}
mkdir -p scripts/{admin,maintenance,deployment}
mkdir -p configs/{dev,prod,staging}
mkdir -p data/{exports,imports,templates}
mkdir -p tests/{unit,integration}
echo -e "${GREEN}✅ Project structure created${NC}"

# Install dependencies
echo -e "${YELLOW}[4/8]${NC} Installing Python dependencies..."
$PYTHON_CMD -m pip install --upgrade pip > /dev/null 2>&1
$PYTHON_CMD -m pip install -r requirements.txt > /dev/null 2>&1
echo -e "${GREEN}✅ Dependencies installed${NC}"

# Setup environment file
echo -e "${YELLOW}[5/8]${NC} Setting up environment configuration..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo -e "${GREEN}✅ .env file created${NC}"
    echo -e "${YELLOW}⚠️  IMPORTANT: Edit .env file and add your tokens!${NC}"
else
    echo -e "${YELLOW}ℹ️  .env file already exists, skipping...${NC}"
fi

# Initialize database
echo -e "${YELLOW}[6/8]${NC} Initializing database..."
$PYTHON_CMD database.py > /dev/null 2>&1
echo -e "${GREEN}✅ Database initialized${NC}"

# Generate dummy data if requested
if [ "$FULL_SETUP" = true ]; then
    echo -e "${YELLOW}[7/8]${NC} Generating dummy data ($NUM_EMPLOYEES employees)..."
    echo "y" | $PYTHON_CMD generate_dummy_data.py $NUM_EMPLOYEES > /dev/null 2>&1
    echo -e "${GREEN}✅ Dummy data generated${NC}"
else
    echo -e "${YELLOW}[7/8]${NC} Skipping dummy data generation (use --full for dummy data)"
fi

# Create quick start scripts
echo -e "${YELLOW}[8/8]${NC} Creating convenience scripts..."

# Windows batch file to start bot
cat > start_bot.bat << 'EOF'
@echo off
echo Starting SDM Bot...
python bot.py
pause
EOF

# Windows batch file for admin tools
cat > admin.bat << 'EOF'
@echo off
echo Starting Admin Tools...
python admin_tools.py
pause
EOF

# Git Bash script to start bot
cat > start.sh << 'EOF'
#!/bin/bash
echo "🤖 Starting SDM Bot..."
python bot.py
EOF
chmod +x start.sh

# Git Bash script for admin
cat > admin.sh << 'EOF'
#!/bin/bash
echo "🛠️  Starting Admin Tools..."
python admin_tools.py
EOF
chmod +x admin.sh

echo -e "${GREEN}✅ Convenience scripts created${NC}"

# Print completion message
echo -e "${BLUE}"
echo "============================================================================"
echo "   ✨ SETUP COMPLETED SUCCESSFULLY!"
echo "============================================================================"
echo -e "${NC}"

echo -e "${GREEN}📋 Next Steps:${NC}"
echo ""
echo "1️⃣  Edit the .env file with your credentials:"
echo "   ${YELLOW}notepad .env${NC}  (or use any text editor)"
echo ""
echo "2️⃣  Get your Telegram Bot Token:"
echo "   • Open Telegram and search for ${YELLOW}@BotFather${NC}"
echo "   • Type ${YELLOW}/newbot${NC} and follow instructions"
echo "   • Copy the token to .env file"
echo ""
echo "3️⃣  Get your Telegram ID:"
echo "   • Open Telegram and search for ${YELLOW}@userinfobot${NC}"
echo "   • Copy your ID to .env file"
echo ""
echo "4️⃣  (Optional) Get OpenAI API Key for AI features:"
echo "   • Visit: ${YELLOW}https://platform.openai.com/${NC}"
echo "   • Generate API key and add to .env"
echo ""
echo "5️⃣  Start the bot:"
echo "   ${GREEN}bash start.sh${NC}  (Git Bash)"
echo "   ${GREEN}start_bot.bat${NC}  (Windows CMD)"
echo "   ${GREEN}python bot.py${NC}  (Direct)"
echo ""
echo "6️⃣  Use admin tools to manage employees:"
echo "   ${GREEN}bash admin.sh${NC}  (Git Bash)"
echo "   ${GREEN}admin.bat${NC}  (Windows CMD)"
echo ""

if [ "$FULL_SETUP" = true ]; then
    echo -e "${GREEN}🎉 BONUS: $NUM_EMPLOYEES dummy employees have been created!${NC}"
    echo "   You can start testing immediately!"
    echo ""
fi

echo -e "${BLUE}📚 Documentation:${NC}"
echo "   • Quick Start: ${YELLOW}QUICKSTART.md${NC}"
echo "   • Full Docs: ${YELLOW}README.md${NC}"
echo "   • Structure: ${YELLOW}PROJECT_STRUCTURE.md${NC}"
echo ""
echo -e "${BLUE}🆘 Need Help?${NC}"
echo "   • Check troubleshooting in QUICKSTART.md"
echo "   • Run: ${YELLOW}python admin_tools.py${NC} for management"
echo ""
echo -e "${GREEN}Happy Coding! 🚀${NC}"
echo ""