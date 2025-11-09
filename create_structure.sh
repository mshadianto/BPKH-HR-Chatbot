#!/bin/bash
# ============================================================================
# CREATE COMPLETE PROJECT STRUCTURE WITH ARTIFACTS
# ============================================================================
# Run: bash create_structure.sh
# ============================================================================

echo "📁 Creating complete project structure with artifacts..."

# Main directories
mkdir -p {docs,scripts,configs,logs,data,backups,tests,assets}

# Subdirectories
mkdir -p docs/{api,guides,screenshots,diagrams}
mkdir -p scripts/{admin,maintenance,deployment,monitoring}
mkdir -p configs/{dev,prod,staging}
mkdir -p data/{exports,imports,templates,cache}
mkdir -p backups/{daily,weekly,monthly}
mkdir -p tests/{unit,integration,e2e}
mkdir -p assets/{images,icons,templates}
mkdir -p logs/{bot,error,audit,performance}

# ============================================================================
# DOCS FOLDER - Documentation artifacts
# ============================================================================

# API Documentation
cat > docs/api/API_REFERENCE.md << 'EOF'
# API Reference - Telegram Bot SDM

## Bot Commands

### User Commands
- `/start` - Start the bot and show main menu
- `/help` - Show help information

### Admin Commands (Admin only)
- `/register` - Register new employee
- `/stats` - View system statistics

## Callback Handlers

### Main Menu Callbacks
- `menu_payroll` - Show payroll menu
- `menu_cuti` - Show leave menu
- `menu_absensi` - Show attendance menu
- `menu_info` - Show employee info
- `menu_bpjs` - Show benefits info
- `menu_kebijakan` - Show policies
- `menu_ai` - Show AI assistant
- `back_main` - Back to main menu

### Payroll Callbacks
- `payroll_current` - Current month salary
- `payroll_history` - Salary history
- `payroll_slip` - Download pay slip

### Cuti Callbacks
- `cuti_saldo` - Check leave balance
- `cuti_ajukan` - Apply for leave
- `cuti_status` - Check leave status
- `cuti_history` - Leave history

### Absensi Callbacks
- `absen_masuk` - Clock in
- `absen_pulang` - Clock out
- `absen_history` - Attendance history
- `absen_summary` - Monthly summary

## Database Models

### Employee
```python
{
    "id": int,
    "telegram_id": str,
    "nip": str,
    "nama": str,
    "email": str,
    "jabatan": str,
    "departemen": str,
    "tanggal_masuk": date,
    "gaji_pokok": float,
    "tunjangan": float,
    "is_active": bool
}
```

### Payroll
```python
{
    "id": int,
    "employee_id": int,
    "periode": str,  # YYYY-MM
    "gaji_pokok": float,
    "tunjangan": float,
    "bonus": float,
    "potongan": float,
    "total_gaji": float,
    "status": str,  # Draft, Processed, Paid
    "tanggal_bayar": date
}
```

### Cuti
```python
{
    "id": int,
    "employee_id": int,
    "jenis_cuti": str,
    "tanggal_mulai": date,
    "tanggal_selesai": date,
    "jumlah_hari": int,
    "alasan": str,
    "status": str,  # Pending, Approved, Rejected
    "approved_by": str
}
```

### Absensi
```python
{
    "id": int,
    "employee_id": int,
    "tanggal": date,
    "jam_masuk": str,
    "jam_keluar": str,
    "status": str,  # Hadir, Izin, Sakit, Alfa
    "keterangan": str
}
```

## RAG Engine

### Query Method
```python
rag_engine.query(question: str) -> str
```

### Add Document Method
```python
rag_engine.add_document(
    kategori: str,
    pertanyaan: str,
    jawaban: str
)
```

## Response Format

### Success Response
```json
{
    "status": "success",
    "data": {},
    "message": "Operation successful"
}
```

### Error Response
```json
{
    "status": "error",
    "error": "Error message",
    "code": 400
}
```
EOF

# User Guide
cat > docs/guides/USER_GUIDE.md << 'EOF'
# User Guide - Bot SDM Telegram

## Getting Started

### 1. First Time Setup
1. Open Telegram
2. Search for your company's bot (e.g., @company_sdm_bot)
3. Click START or type `/start`
4. If not registered, contact HR

### 2. Main Menu Overview

When you start the bot, you'll see these menus:

#### 1️⃣ Payroll
- Check current month salary
- View salary history
- Download pay slip

#### 2️⃣ Cuti (Leave)
- Check remaining leave days
- Apply for leave
- Track leave request status
- View leave history

#### 3️⃣ Absensi (Attendance)
- Clock in (when arriving at work)
- Clock out (when leaving work)
- View attendance history
- Monthly attendance summary

#### 4️⃣ Info Karyawan
- View your personal information
- Check employment details

#### 5️⃣ BPJS & Benefit
- BPJS information
- Employee benefits
- How to claim benefits

#### 6️⃣ Kebijakan HR
- Company policies
- Working hours
- Dress code
- WFH policy

#### 💬 Tanya AI
- Ask questions about company policies
- Get instant answers from AI

## Common Tasks

### How to Check Your Salary
1. Click `1️⃣ Payroll`
2. Click `💰 Gaji Bulan Ini`
3. View your salary details

### How to Apply for Leave
1. Click `2️⃣ Cuti`
2. Click `✍️ Ajukan Cuti`
3. Select leave type (1, 2, or 3)
4. Follow the prompts to enter:
   - Start date
   - End date
   - Reason
5. Wait for approval

### How to Clock In/Out
1. Click `3️⃣ Absensi`
2. Click `✅ Absen Masuk` (in the morning)
3. Click `🏃 Absen Pulang` (when leaving)

### How to Ask AI
1. Click `💬 Tanya AI`
2. Type your question, for example:
   - "Kapan gaji dibayarkan?"
   - "Bagaimana cara mengajukan cuti?"
   - "Berapa hari cuti tahunan?"
3. Get instant answer from AI

## Tips & Tricks

✅ **Daily Routine**
- Clock in when you arrive (before 8:15 AM)
- Clock out when you leave
- Type `/start` anytime to return to main menu

✅ **Leave Application**
- Apply at least 3 days in advance
- For emergency leave, inform your manager immediately

✅ **Salary Queries**
- Salary is paid on the 25th of each month
- Check your payslip via the bot

✅ **Using AI Assistant**
- Ask in Indonesian language
- Be specific with your questions
- AI knows all company policies

## Troubleshooting

### Bot not responding?
- Make sure you've started the bot with `/start`
- Check your internet connection
- Try restarting the bot

### Can't find your data?
- You might not be registered yet
- Contact HR department

### Leave request not showing?
- Check the status under `📋 Status Pengajuan`
- It may take 1-3 days for approval

## Contact Support

For technical issues:
- Email: hrd@perusahaan.com
- Phone: 021-12345678
- WhatsApp: 0812-3456-7890

## Frequently Asked Questions

**Q: Can I use the bot outside office hours?**
A: Yes, the bot is available 24/7.

**Q: Is my data secure?**
A: Yes, all data is encrypted and secure.

**Q: Can I edit my leave request?**
A: No, you need to cancel and submit a new one.

**Q: What if I forget to clock in?**
A: Contact your manager or HR immediately.
EOF

# Admin Guide
cat > docs/guides/ADMIN_GUIDE.md << 'EOF'
# Admin Guide - Bot SDM Telegram

## Admin Tools Overview

The admin tools (`admin_tools.py`) provide a CLI interface for managing the HR system.

## Starting Admin Tools

### Windows
```bash
admin.bat
```

### Git Bash / Linux
```bash
bash admin.sh
# or
python admin_tools.py
```

## Admin Menu

```
1. Registrasi Karyawan Baru
2. Lihat Daftar Karyawan
3. Non-aktifkan Karyawan
4. Approve/Reject Cuti
5. Generate Payroll Bulanan
6. Lihat Statistik
0. Keluar
```

## 1. Register New Employee

Steps:
1. Select menu `1`
2. Enter employee details:
   - Telegram ID (get from @userinfobot)
   - NIP (unique employee number)
   - Full name
   - Email
   - Position
   - Department
   - Join date (YYYY-MM-DD)
   - Base salary
   - Allowance
3. Confirm the data
4. Employee can now use the bot

**Example:**
```
Telegram ID: 123456789
NIP: EMP001
Nama Lengkap: John Doe
Email: john.doe@company.com
Jabatan: Senior Developer
Departemen: IT
Tanggal Masuk: 2024-01-15
Gaji Pokok: 12000000
Tunjangan: 3000000
```

## 2. View Employee List

Shows all employees with:
- NIP
- Name
- Position
- Status (Active/Inactive)

## 3. Deactivate Employee

For employees who resign or are terminated:
1. Select menu `3`
2. Enter employee NIP
3. Confirm deactivation
4. Employee status changed to inactive

## 4. Approve/Reject Leave

Review and process leave requests:
1. Select menu `4`
2. View list of pending leave requests
3. Enter leave ID to process
4. Choose: Approve (a) or Reject (r)
5. Enter approver name
6. Employee will be notified

## 5. Generate Monthly Payroll

Create payroll for all active employees:
1. Select menu `5`
2. Confirm the period (current month)
3. Enter bonus for each employee (if any)
4. System calculates deductions automatically
5. Payroll records created

**Automatic Calculations:**
- Base salary + Allowance + Bonus
- Deductions (5% default for BPJS + tax)
- Total salary

## 6. View Statistics

Dashboard showing:
- Total active employees
- Total departments
- Pending leave requests
- Monthly attendance count
- Employees per department

## Best Practices

### Daily Tasks
- ✅ Check pending leave requests
- ✅ Monitor attendance
- ✅ Respond to employee queries

### Weekly Tasks
- ✅ Review attendance patterns
- ✅ Process approved leave requests
- ✅ Update employee information if needed

### Monthly Tasks
- ✅ Generate monthly payroll
- ✅ Review performance metrics
- ✅ Generate reports

## Database Management

### Backup Database
```bash
# Create backup
cp sdm_database.db backups/sdm_backup_$(date +%Y%m%d).db
```

### Restore Database
```bash
# Restore from backup
cp backups/sdm_backup_20240101.db sdm_database.db
```

## Troubleshooting

### Employee can't use bot
1. Check if registered in system
2. Verify Telegram ID is correct
3. Check employee status (must be active)

### Leave approval not working
1. Verify leave ID exists
2. Check leave status (must be Pending)
3. Ensure approver name is entered

### Payroll generation fails
1. Check all employees have salary data
2. Verify period format (YYYY-MM)
3. Check for duplicate payroll records

## Security

### Admin Access
- Only authorized personnel should have access
- Keep admin credentials secure
- Log all admin actions

### Data Protection
- Regular backups (daily recommended)
- Encrypt sensitive data
- Follow data retention policies

## Support

For admin tool issues:
- Check error logs: `logs/error.log`
- Contact IT support
- Refer to technical documentation
EOF

# ============================================================================
# SCRIPTS FOLDER - Utility scripts
# ============================================================================

# Backup script
cat > scripts/maintenance/backup.sh << 'EOF'
#!/bin/bash
# Database Backup Script

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="backups/daily"
mkdir -p $BACKUP_DIR

echo "🔄 Creating backup..."

# Backup database
cp sdm_database.db "$BACKUP_DIR/sdm_db_$DATE.db"

# Backup .env (without secrets)
grep -v "TOKEN\|KEY\|PASSWORD" .env > "$BACKUP_DIR/config_$DATE.env" 2>/dev/null || true

# Compress logs
tar -czf "$BACKUP_DIR/logs_$DATE.tar.gz" logs/ 2>/dev/null || true

echo "✅ Backup completed: $BACKUP_DIR"
echo "   - Database: sdm_db_$DATE.db"
echo "   - Logs: logs_$DATE.tar.gz"

# Remove old backups (keep 30 days)
find $BACKUP_DIR -name "*.db" -mtime +30 -delete 2>/dev/null || true
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete 2>/dev/null || true

echo "🗑️  Old backups cleaned (kept last 30 days)"
EOF
chmod +x scripts/maintenance/backup.sh

# Monitor script
cat > scripts/monitoring/health_check.sh << 'EOF'
#!/bin/bash
# Health Check Script

echo "🏥 Health Check - SDM Bot"
echo "=========================="

# Check if bot is running
if pgrep -f "bot.py" > /dev/null; then
    echo "✅ Bot Status: RUNNING"
else
    echo "❌ Bot Status: NOT RUNNING"
    echo "   Run: python bot.py"
fi

# Check database
if [ -f "sdm_database.db" ]; then
    DB_SIZE=$(du -h sdm_database.db | cut -f1)
    echo "✅ Database: OK ($DB_SIZE)"
else
    echo "❌ Database: NOT FOUND"
fi

# Check logs
if [ -d "logs" ]; then
    LOG_COUNT=$(find logs -name "*.log" | wc -l)
    echo "✅ Logs: $LOG_COUNT files"
else
    echo "⚠️  Logs: Directory not found"
fi

# Check Python packages
echo ""
echo "📦 Package Status:"
python -c "import telegram; print('✅ python-telegram-bot:', telegram.__version__)" 2>/dev/null || echo "❌ python-telegram-bot: NOT INSTALLED"
python -c "import langchain; print('✅ langchain: OK')" 2>/dev/null || echo "❌ langchain: NOT INSTALLED"
python -c "import openai; print('✅ openai: OK')" 2>/dev/null || echo "❌ openai: NOT INSTALLED"

echo ""
echo "=========================="
EOF
chmod +x scripts/monitoring/health_check.sh

# ============================================================================
# CONFIGS FOLDER - Configuration examples
# ============================================================================

# Development config
cat > configs/dev/config.yaml << 'EOF'
# Development Configuration
environment: development

database:
  type: sqlite
  name: sdm_database.db
  echo: true  # Show SQL queries

bot:
  polling_interval: 1.0
  timeout: 30
  debug: true

rag:
  model: gpt-3.5-turbo
  temperature: 0.3
  max_tokens: 1000

logging:
  level: DEBUG
  file: logs/bot_dev.log
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

features:
  ai_enabled: true
  caching: false
  rate_limiting: false
EOF

# Production config
cat > configs/prod/config.yaml << 'EOF'
# Production Configuration
environment: production

database:
  type: postgresql
  host: localhost
  port: 5432
  name: sdm_prod
  echo: false

bot:
  webhook_url: https://bot.company.com/webhook
  webhook_port: 8443
  timeout: 60
  debug: false

rag:
  model: gpt-4
  temperature: 0.2
  max_tokens: 2000

logging:
  level: INFO
  file: logs/bot_prod.log
  format: "%(asctime)s - %(levelname)s - %(message)s"

features:
  ai_enabled: true
  caching: true
  rate_limiting: true
  rate_limit: 100  # requests per hour

security:
  encrypt_db: true
  ssl_enabled: true
  admin_ips: ["192.168.1.100", "192.168.1.101"]
EOF

# ============================================================================
# DATA FOLDER - Templates
# ============================================================================

# CSV template for bulk employee import
cat > data/templates/employee_import_template.csv << 'EOF'
telegram_id,nip,nama,email,jabatan,departemen,tanggal_masuk,gaji_pokok,tunjangan
123456789,EMP001,John Doe,john@company.com,Senior Developer,IT,2024-01-15,12000000,3000000
987654321,EMP002,Jane Smith,jane@company.com,HR Manager,HR,2024-01-20,15000000,4000000
EOF

# Leave request template
cat > data/templates/leave_request_template.txt << 'EOF'
FORMULIR PENGAJUAN CUTI

Nama              : _______________________________
NIP               : _______________________________
Departemen        : _______________________________
Jenis Cuti        : [ ] Tahunan  [ ] Sakit  [ ] Penting

Tanggal Mulai     : ___/___/______
Tanggal Selesai   : ___/___/______
Jumlah Hari       : _____ hari

Alasan            : _______________________________
                    _______________________________
                    _______________________________

Tanggal Pengajuan : ___/___/______
Tanda Tangan      : _______________________________

                    Persetujuan

Atasan Langsung   : _______________________________
Tanggal           : ___/___/______
Tanda Tangan      : _______________________________

HRD               : _______________________________
Tanggal           : ___/___/______
Tanda Tangan      : _______________________________
EOF

# ============================================================================
# TESTS FOLDER - Test examples
# ============================================================================

cat > tests/unit/test_database.py << 'EOF'
"""
Unit tests for database models
Run: python -m pytest tests/unit/test_database.py
"""

import unittest
from datetime import date
from database import Employee, Cuti, Absensi, Payroll

class TestEmployeeModel(unittest.TestCase):
    def test_employee_creation(self):
        emp = Employee(
            telegram_id="123456",
            nip="EMP001",
            nama="Test User",
            email="test@example.com",
            jabatan="Developer",
            departemen="IT",
            tanggal_masuk=date.today(),
            gaji_pokok=10000000,
            tunjangan=2000000,
            is_active=True
        )
        self.assertEqual(emp.nama, "Test User")
        self.assertTrue(emp.is_active)

class TestCutiModel(unittest.TestCase):
    def test_cuti_creation(self):
        cuti = Cuti(
            employee_id=1,
            jenis_cuti="Cuti Tahunan",
            tanggal_mulai=date.today(),
            tanggal_selesai=date.today(),
            jumlah_hari=1,
            alasan="Test",
            status="Pending"
        )
        self.assertEqual(cuti.status, "Pending")

if __name__ == '__main__':
    unittest.main()
EOF

# ============================================================================
# CREATE README FOR EACH FOLDER
# ============================================================================

cat > docs/README.md << 'EOF'
# Documentation Folder

This folder contains all project documentation.

## Contents

- `api/` - API reference and endpoints
- `guides/` - User and admin guides
- `screenshots/` - UI screenshots
- `diagrams/` - System architecture diagrams
EOF

cat > scripts/README.md << 'EOF'
# Scripts Folder

Utility scripts for maintenance and deployment.

## Usage

### Maintenance
- `maintenance/backup.sh` - Database backup
- `maintenance/cleanup.sh` - Clean old logs

### Monitoring  
- `monitoring/health_check.sh` - System health check
EOF

cat > configs/README.md << 'EOF'
# Configuration Folder

Environment-specific configurations.

## Environments

- `dev/` - Development settings
- `prod/` - Production settings
- `staging/` - Staging environment
EOF

cat > data/README.md << 'EOF'
# Data Folder

Templates and data files.

## Contents

- `templates/` - CSV and document templates
- `exports/` - Exported reports
- `imports/` - Data import files
EOF

cat > tests/README.md << 'EOF'
# Tests Folder

Test suites for the application.

## Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run unit tests only
python -m pytest tests/unit/

# Run integration tests
python -m pytest tests/integration/
```
EOF

cat > logs/README.md << 'EOF'
# Logs Folder

Application logs are stored here.

## Log Files

- `bot/` - Bot operation logs
- `error/` - Error logs
- `audit/` - Audit trail
- `performance/` - Performance metrics

Note: Log files are automatically created when the bot runs.
EOF

echo "✅ Complete project structure created!"
echo ""
echo "📁 Folder Structure:"
echo "   ├── docs/         (Documentation)"
echo "   ├── scripts/      (Utility scripts)"
echo "   ├── configs/      (Configurations)"
echo "   ├── data/         (Templates & data)"
echo "   ├── logs/         (Log files)"
echo "   ├── backups/      (Backup files)"
echo "   ├── tests/        (Test suites)"
echo "   └── assets/       (Images & resources)"
echo ""
echo "🎉 All artifacts created successfully!"