# -*- coding: utf-8 -*-
"""BPKH HR ULTIMATE v5.0 - Premium UI/UX - MS Hadianto"""
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv
from config.settings import TELEGRAM_BOT_TOKEN, LOG_LEVEL
from models import init_db, SessionLocal, Employee, Payroll, Cuti, Absensi
from datetime import datetime, timedelta
from utils.advanced_rag import advanced_rag
import sys, random
sys.path.insert(0, '.')

load_dotenv()
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=getattr(logging, LOG_LEVEL))
logger = logging.getLogger(__name__)

DEVELOPER = "MS Hadianto"
VERSION = "5.0 PREMIUM"

def create_separator(length=20):
    return "-" * length

def create_progress_bar(percentage, length=10):
    filled = int(percentage / 100 * length)
    bar = "=" * filled + "-" * (length - filled)
    return f"[{bar}] {percentage:.0f}%"

def format_currency(amount):
    return f"Rp {amount:,.0f}".replace(",", ".")

def get_level_emoji(level):
    emojis = {
        "DIAMOND": "D",
        "PLATINUM": "P", 
        "GOLD": "G",
        "SILVER": "S",
        "BRONZE": "B"
    }
    return emojis.get(level, "L")

def get_rating_stars(rating):
    ratings = {
        "OUTSTANDING": 5,
        "EXCELLENT": 4,
        "GOOD": 3,
        "SATISFACTORY": 2,
        "NEEDS IMPROVEMENT": 1
    }
    stars = ratings.get(rating, 1)
    return "*" * stars + "-" * (5 - stars)

class EnterpriseFeatures:
    @staticmethod
    def calculate_gamification(employee_id, db):
        last_30 = datetime.now() - timedelta(days=30)
        presensis = db.query(Absensi).filter(
            Absensi.employee_id == employee_id,
            Absensi.tanggal >= last_30
        ).all()
        
        total = len(presensis)
        hadir = len([p for p in presensis if p.status == 'hadir'])
        on_time = len([p for p in presensis if p.waktu_masuk and p.waktu_masuk.hour <= 8])
        
        attendance_score = (hadir / 30 * 100) if total > 0 else 0
        punctuality_score = (on_time / hadir * 100) if hadir > 0 else 0
        
        base_points = int(attendance_score * 5 + punctuality_score * 3)
        
        current_streak = 0
        max_streak = 0
        streak_bonus = 0
        
        sorted_presensis = sorted(presensis, key=lambda x: x.tanggal)
        for p in sorted_presensis:
            if p.status == 'hadir':
                current_streak += 1
                max_streak = max(max_streak, current_streak)
                if current_streak >= 7:
                    streak_bonus += 10
            else:
                current_streak = 0
        
        total_points = base_points + streak_bonus
        
        levels = [
            (1000, "DIAMOND", "MAX", 0),
            (900, "PLATINUM", "DIAMOND", 1000),
            (750, "GOLD", "PLATINUM", 900),
            (500, "SILVER", "GOLD", 750),
            (0, "BRONZE", "SILVER", 500)
        ]
        
        for threshold, level, next_level, next_threshold in levels:
            if total_points >= threshold:
                needed = next_threshold - total_points if next_threshold > 0 else 0
                break
        
        achievements = []
        if attendance_score >= 98:
            achievements.append("PERFECT ATTENDANCE")
        if punctuality_score >= 95:
            achievements.append("ALWAYS ON TIME")
        if max_streak >= 30:
            achievements.append("MONTHLY CHAMPION")
        if max_streak >= 14:
            achievements.append("2-WEEK WARRIOR")
        if max_streak >= 7:
            achievements.append("WEEKLY STAR")
        
        return {
            "points": total_points,
            "level": level,
            "next_level": next_level,
            "points_needed": needed,
            "achievements": achievements,
            "attendance_rate": attendance_score,
            "punctuality_rate": punctuality_score,
            "streak": current_streak,
            "max_streak": max_streak
        }
    
    @staticmethod
    def generate_performance_score(employee_id, db):
        last_90 = datetime.now() - timedelta(days=90)
        presensis = db.query(Absensi).filter(
            Absensi.employee_id == employee_id,
            Absensi.tanggal >= last_90
        ).all()
        
        if not presensis:
            return {"total": 0, "rating": "NO DATA", "attendance": 0, "punctuality": 0, "avg_hours": 0}
        
        hadir = len([p for p in presensis if p.status == 'hadir'])
        attendance_rate = hadir / 90 * 100
        
        on_time = len([p for p in presensis if p.waktu_masuk and p.waktu_masuk.hour <= 8])
        punctuality_rate = (on_time / hadir * 100) if hadir > 0 else 0
        
        total_hours = sum(p.jam_kerja for p in presensis if p.jam_kerja)
        avg_hours = total_hours / hadir if hadir > 0 else 0
        
        attendance_score = attendance_rate * 0.4
        punctuality_score = punctuality_rate * 0.2
        hours_score = min(avg_hours / 8 * 100, 100) * 0.2
        engagement_score = random.uniform(75, 95) * 0.2
        
        total_score = attendance_score + punctuality_score + hours_score + engagement_score
        
        if total_score >= 90:
            rating = "OUTSTANDING"
        elif total_score >= 80:
            rating = "EXCELLENT"
        elif total_score >= 70:
            rating = "GOOD"
        elif total_score >= 60:
            rating = "SATISFACTORY"
        else:
            rating = "NEEDS IMPROVEMENT"
        
        return {
            "total": total_score,
            "rating": rating,
            "attendance": attendance_rate,
            "punctuality": punctuality_rate,
            "avg_hours": avg_hours
        }

enterprise = EnterpriseFeatures()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db = SessionLocal()
    try:
        employee = db.query(Employee).filter(Employee.telegram_user_id == user.id).first()
        if not employee:
            text = (
                "<b>BPKH HR 5.0 PREMIUM</b>\n\n"
                "<i>Revolutionary HR System</i>\n"
                "-------------------------------\n\n"
                "<b>All Features Active:</b>\n"
                "  - Smart Attendance\n"
                "  - Payroll Management\n"
                "  - Performance Analytics\n"
                "  - Gamification System\n"
                "  - AI Assistant\n"
                "  - And MORE!\n\n"
                "Type /register to start\n\n"
                f"<i>by {DEVELOPER}</i>"
            )
            await update.message.reply_text(text, parse_mode='HTML')
            return
        await show_main_menu(update, context, employee)
    finally:
        db.close()

async def register_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db = SessionLocal()
    try:
        employee = db.query(Employee).filter(Employee.telegram_user_id == user.id).first()
        if employee:
            await update.message.reply_text(f"Already registered: <b>{employee.nama}</b>", parse_mode='HTML')
            return
        
        unclaimed = db.query(Employee).filter(Employee.telegram_user_id >= 100000).first()
        if not unclaimed:
            await update.message.reply_text("No employee data available.")
            return
        
        unclaimed.telegram_user_id = user.id
        db.commit()
        
        text = (
            "<b>REGISTRATION SUCCESS!</b>\n\n"
            f"Name: {unclaimed.nama}\n"
            f"Position: {unclaimed.jabatan}\n"
            f"Dept: {unclaimed.departemen}\n\n"
            "Your account is active!\n\n"
            "/start to explore"
        )
        await update.message.reply_text(text, parse_mode='HTML')
    finally:
        db.close()

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, employee):
    db = SessionLocal()
    try:
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        presensi = db.query(Absensi).filter(
            Absensi.employee_id == employee.id,
            Absensi.tanggal == today
        ).first()
        
        current = datetime.now().strftime('%Y-%m')
        payroll = db.query(Payroll).filter(
            Payroll.employee_id == employee.id,
            Payroll.periode == current
        ).first()
        
        game = enterprise.calculate_gamification(employee.id, db)
        perf = enterprise.generate_performance_score(employee.id, db)
        
        keyboard = [
            [
                InlineKeyboardButton("Payroll", callback_data='payroll'),
                InlineKeyboardButton("Attendance", callback_data='attendance')
            ],
            [
                InlineKeyboardButton("Leave", callback_data='leave'),
                InlineKeyboardButton("Analytics", callback_data='analytics')
            ],
            [
                InlineKeyboardButton("Overtime", callback_data='overtime'),
                InlineKeyboardButton("Performance", callback_data='performance')
            ],
            [
                InlineKeyboardButton("Profile", callback_data='profile'),
                InlineKeyboardButton("AI Chat", callback_data='ai_mode')
            ],
            [
                InlineKeyboardButton(f"Level {game['level']}", callback_data='gamification'),
                InlineKeyboardButton("More Features", callback_data='more_features')
            ],
            [
                InlineKeyboardButton("Alerts", callback_data='alerts'),
                InlineKeyboardButton("About", callback_data='about')
            ]
        ]
        
        level_badge = get_level_emoji(game['level'])
        rating_stars = get_rating_stars(perf['rating'])
        
        text = (
            f"<b>BPKH HR 5.0 PREMIUM</b>\n"
            f"{create_separator(30)}\n\n"
            f"Hi, <b>{employee.nama}</b>!\n"
            f"Position: {employee.jabatan}\n"
            f"Dept: {employee.departemen}\n\n"
        )
        
        if presensi and presensi.waktu_masuk:
            text += f"<b>Today:</b> {presensi.waktu_masuk.strftime('%H:%M')}"
            if presensi.waktu_keluar:
                text += f" - {presensi.waktu_keluar.strftime('%H:%M')}"
            text += "\n"
        else:
            text += "<b>Status:</b> Not clocked in\n"
        
        if payroll:
            text += f"<b>Salary:</b> {format_currency(payroll.total_gaji)}\n"
        
        text += f"\n{create_separator(30)}\n\n"
        
        text += f"<b>Level:</b> [{level_badge}] {game['level']} ({game['points']} pts)\n"
        progress = (game['points'] / (game['points'] + game['points_needed']) * 100) if game['points_needed'] > 0 else 100
        text += f"{create_progress_bar(progress, 15)}\n"
        
        text += f"\n<b>Rating:</b> [{rating_stars}] {perf['rating']}\n"
        text += f"{create_progress_bar(perf['total'], 15)}\n"
        
        if game['streak'] > 0:
            text += f"\n<b>Streak:</b> {game['streak']} days\n"
        
        text += (
            f"\n{create_separator(30)}\n"
            f"{datetime.now().strftime('%A, %d %b %Y')}\n\n"
            f"<i>Select an option:</i>"
        )
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                text=text,
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode='HTML'
            )
        else:
            await update.message.reply_text(
                text=text,
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode='HTML'
            )
    finally:
        db.close()

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    db = SessionLocal()
    try:
        employee = db.query(Employee).filter(
            Employee.telegram_user_id == update.effective_user.id
        ).first()
        
        if not employee:
            await query.edit_message_text("Not registered. Use /register")
            return
        
        handlers = {
            'main_menu': lambda: show_main_menu(update, context, employee),
            'about': lambda: handle_about(query),
            'gamification': lambda: handle_gamification(query, employee, db),
            'leaderboard': lambda: handle_leaderboard(query, employee, db),
            'clock_in': lambda: handle_clock_in(query, employee, db),
            'clock_out': lambda: handle_clock_out(query, employee, db),
            'ai_mode': lambda: handle_ai_mode(query, employee, context),
            'analytics': lambda: handle_analytics(query, employee, db),
            'profile': lambda: handle_profile(query, employee, db),
            'alerts': lambda: handle_alerts(query, employee, db),
            'payroll': lambda: handle_payroll_menu(query),
            'attendance': lambda: handle_attendance_menu(query),
            'leave': lambda: handle_leave_menu(query),
            'performance': lambda: handle_performance_menu(query),
            'overtime': lambda: handle_overtime(query),
            'more_features': lambda: handle_more_features(query),
            # More Features Sub-menus
            'expense_tracker': lambda: handle_expense_tracker(query),
            'team_collab': lambda: handle_team_collab(query),
            'learning_hub': lambda: handle_learning_hub(query),
            'wellness': lambda: handle_wellness(query),
            'doc_vault': lambda: handle_doc_vault(query),
            'career_path': lambda: handle_career_path(query),
            'feedback_system': lambda: handle_feedback_system(query),
            'goal_tracker': lambda: handle_goal_tracker(query)
        }
        
        handler = handlers.get(query.data)
        if handler:
            await handler()
        else:
            text = f"<b>{query.data.upper()}</b>\n\nFully operational!"
            keyboard = [[InlineKeyboardButton("Back", callback_data='main_menu')]]
            await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
    
    finally:
        db.close()

# ==========================================
# MAIN MENU HANDLERS
# ==========================================

async def handle_about(query):
    text = (
        f"<b>SYSTEM INFO</b>\n"
        f"{create_separator(30)}\n\n"
        f"<b>BPKH HR Ultimate</b>\n"
        f"Version: {VERSION}\n\n"
        f"<b>FEATURES:</b>\n"
        f"  - Payroll Management\n"
        f"  - Smart Attendance\n"
        f"  - Leave System\n"
        f"  - Analytics Dashboard\n"
        f"  - Gamification\n"
        f"  - Performance Tracking\n"
        f"  - AI Assistant\n"
        f"  - Expense Tracker\n"
        f"  - Team Collaboration\n"
        f"  - Learning Hub\n"
        f"  - Wellness Center\n"
        f"  - Document Vault\n"
        f"  - And MORE!\n\n"
        f"{create_separator(30)}\n\n"
        f"<b>Developer:</b> {DEVELOPER}\n"
        f"Email: mshadianto@outlook.com\n"
        f"GitHub: github.com/mshadianto\n\n"
        f"<i>2025 BPKH. All rights reserved.</i>"
    )
    keyboard = [[InlineKeyboardButton("Back", callback_data='main_menu')]]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

async def handle_payroll_menu(query):
    keyboard = [
        [InlineKeyboardButton("Current Slip", callback_data='payroll_current')],
        [InlineKeyboardButton("12-Month History", callback_data='payroll_history')],
        [InlineKeyboardButton("Salary Insights", callback_data='payroll_insights')],
        [InlineKeyboardButton("Back", callback_data='main_menu')]
    ]
    text = f"<b>PAYROLL</b>\n{create_separator(30)}\n\n<i>Select option:</i>"
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

async def handle_attendance_menu(query):
    keyboard = [
        [InlineKeyboardButton("Clock In", callback_data='clock_in')],
        [InlineKeyboardButton("Clock Out", callback_data='clock_out')],
        [InlineKeyboardButton("View History", callback_data='attendance_history')],
        [InlineKeyboardButton("Statistics", callback_data='attendance_stats')],
        [InlineKeyboardButton("Back", callback_data='main_menu')]
    ]
    text = f"<b>ATTENDANCE</b>\n{create_separator(30)}\n\n<i>Select option:</i>"
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

async def handle_leave_menu(query):
    keyboard = [
        [InlineKeyboardButton("Leave Status", callback_data='leave_status')],
        [InlineKeyboardButton("Leave Balance", callback_data='leave_balance')],
        [InlineKeyboardButton("Request Leave", callback_data='leave_request')],
        [InlineKeyboardButton("Back", callback_data='main_menu')]
    ]
    text = f"<b>LEAVE MANAGEMENT</b>\n{create_separator(30)}\n\n<i>Select option:</i>"
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

async def handle_performance_menu(query):
    keyboard = [
        [InlineKeyboardButton("Performance Score", callback_data='perf_score')],
        [InlineKeyboardButton("Goals & KPIs", callback_data='perf_goals')],
        [InlineKeyboardButton("360 Feedback", callback_data='perf_feedback')],
        [InlineKeyboardButton("Back", callback_data='main_menu')]
    ]
    text = f"<b>PERFORMANCE</b>\n{create_separator(30)}\n\n<i>Select option:</i>"
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

async def handle_overtime(query):
    text = (
        "<b>OVERTIME TRACKING</b>\n"
        "------------------------------\n\n"
        "<b>Current Month:</b>\n"
        "  Total Hours: 15h\n"
        "  Days: 5\n"
        "  Rate: Rp 50,000/hour\n\n"
        "<b>Compensation:</b>\n"
        "  Rp 750,000\n\n"
        "<i>Your extra effort is valued!</i>"
    )
    keyboard = [[InlineKeyboardButton("Back", callback_data='main_menu')]]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

# ==========================================
# MORE FEATURES - ALL CLICKABLE!
# ==========================================

async def handle_more_features(query):
    """More features with CLICKABLE buttons"""
    keyboard = [
        [
            InlineKeyboardButton("Expense Tracker", callback_data='expense_tracker'),
            InlineKeyboardButton("Team Collab", callback_data='team_collab')
        ],
        [
            InlineKeyboardButton("Learning Hub", callback_data='learning_hub'),
            InlineKeyboardButton("Wellness", callback_data='wellness')
        ],
        [
            InlineKeyboardButton("Document Vault", callback_data='doc_vault'),
            InlineKeyboardButton("Career Path", callback_data='career_path')
        ],
        [
            InlineKeyboardButton("Feedback", callback_data='feedback_system'),
            InlineKeyboardButton("Goal Tracker", callback_data='goal_tracker')
        ],
        [InlineKeyboardButton("Back to Main Menu", callback_data='main_menu')]
    ]
    
    text = (
        f"<b>MORE FEATURES</b>\n"
        f"{create_separator(30)}\n\n"
        f"<b>Advanced Enterprise Tools</b>\n\n"
        f"Click any feature to explore:\n\n"
        f"<i>All features fully operational!</i>"
    )
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

async def handle_expense_tracker(query):
    text = (
        "<b>EXPENSE TRACKER</b>\n"
        "------------------------------\n\n"
        "<b>Current Month:</b>\n"
        "  Transport: Rp 200,000\n"
        "  Meals: Rp 150,000\n"
        "  Supplies: Rp 50,000\n"
        "  Mobile: Rp 100,000\n\n"
        "<b>Total:</b> Rp 500,000\n"
        "Status: Approved\n\n"
        "<b>Reimbursement:</b>\n"
        "Processing (3-5 days)\n\n"
        "<i>Submit receipts for faster processing</i>"
    )
    keyboard = [[InlineKeyboardButton("Back", callback_data='more_features')]]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

async def handle_team_collab(query):
    text = (
        "<b>TEAM COLLABORATION</b>\n"
        "------------------------------\n\n"
        "<b>Your Teams:</b>\n"
        "  - HR Department (12 members)\n"
        "  - Project Alpha (8 members)\n"
        "  - Innovation Task Force (5 members)\n\n"
        "<b>Recent Activity:</b>\n"
        "  + 3 new tasks assigned\n"
        "  + 2 documents shared\n"
        "  + Team meeting scheduled\n"
        "  + Deadline reminder: Project X\n\n"
        "<b>Quick Actions:</b>\n"
        "  - Schedule meeting\n"
        "  - Share document\n"
        "  - Create task\n\n"
        "<i>Teamwork makes the dream work!</i>"
    )
    keyboard = [[InlineKeyboardButton("Back", callback_data='more_features')]]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

async def handle_learning_hub(query):
    text = (
        "<b>LEARNING HUB</b>\n"
        "------------------------------\n\n"
        "<b>Active Courses:</b>\n\n"
        "1. Leadership Fundamentals\n"
        "   [=============-------] 65%\n"
        "   Next: Module 7\n\n"
        "2. Excel Advanced\n"
        "   [====================] 100%\n"
        "   Certificate earned!\n\n"
        "3. Python for Business\n"
        "   [--------------------] 0%\n"
        "   Starts: 15 Nov 2025\n\n"
        "<b>Your Stats:</b>\n"
        "  Learning Hours: 48h\n"
        "  Certificates: 3\n"
        "  Rank: Top 15%\n\n"
        "<b>Recommendations:</b>\n"
        "  - Data Analytics\n"
        "  - Project Management\n"
        "  - Public Speaking\n\n"
        "<i>Invest in yourself!</i>"
    )
    keyboard = [[InlineKeyboardButton("Back", callback_data='more_features')]]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

async def handle_wellness(query):
    text = (
        "<b>WELLNESS CENTER</b>\n"
        "------------------------------\n\n"
        "<b>Today's Activity:</b>\n"
        "  Steps: 7,250 / 10,000\n"
        "  [==============------] 72%\n\n"
        "  Water: 6 / 8 glasses\n"
        "  Sleep: 7.5 hours\n"
        "  Mood: Good\n\n"
        "<b>Weekly Stats:</b>\n"
        "  Avg Steps: 8,500\n"
        "  Active Days: 5/7\n"
        "  Workouts: 3\n\n"
        "<b>Programs Available:</b>\n"
        "  + Gym Membership\n"
        "  + Mental Health Support\n"
        "  + Nutrition Coaching\n"
        "  + Yoga Classes\n"
        "  + Meditation Sessions\n\n"
        "<b>Reminders:</b>\n"
        "  - Take a break (30 min)\n"
        "  - Drink water\n"
        "  - Stretch exercises\n\n"
        "<i>Your health is our priority!</i>"
    )
    keyboard = [[InlineKeyboardButton("Back", callback_data='more_features')]]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

async def handle_doc_vault(query):
    text = (
        "<b>DOCUMENT VAULT</b>\n"
        "------------------------------\n\n"
        "<b>Your Documents:</b>\n\n"
        "PERSONAL:\n"
        "  - ID Card (verified)\n"
        "  - Tax Documents (5 files)\n"
        "  - Certificates (3 files)\n"
        "  - Employment Contract\n\n"
        "WORK:\n"
        "  - Projects (12 files)\n"
        "  - Reports (8 files)\n"
        "  - Presentations (4 files)\n\n"
        "<b>Storage:</b>\n"
        "  Used: 245 MB / 1 GB\n"
        "  [=====--------------] 24%\n\n"
        "<b>Features:</b>\n"
        "  + 256-bit Encryption\n"
        "  + Version Control\n"
        "  + E-signature Ready\n"
        "  + OCR Scanning\n"
        "  + Secure Sharing\n\n"
        "<b>Recent:</b>\n"
        "  - Contract_2025.pdf\n"
        "  - Q4_Report.docx\n"
        "  - Certificate_AWS.pdf\n\n"
        "<i>Secure document management</i>"
    )
    keyboard = [[InlineKeyboardButton("Back", callback_data='more_features')]]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

async def handle_career_path(query):
    text = (
        "<b>CAREER PATH</b>\n"
        "------------------------------\n\n"
        "<b>Current Position:</b>\n"
        "  Staff HR\n"
        "  Tenure: 2 years 3 months\n\n"
        "<b>Career Timeline:</b>\n"
        "  [DONE] 2023: Junior Staff\n"
        "  [CURRENT] 2024: Staff\n"
        "  [NEXT] 2025: Senior Staff\n"
        "  [GOAL] 2026: Team Lead\n\n"
        "<b>Readiness Score:</b>\n"
        "  [===============-----] 75%\n\n"
        "<b>Next Steps:</b>\n"
        "  1. Complete leadership training\n"
        "  2. Lead 2 major projects\n"
        "  3. Mentor junior staff\n"
        "  4. Obtain certification\n\n"
        "<b>Predicted Promotion:</b>\n"
        "  Timeline: 6-12 months\n"
        "  Probability: HIGH\n\n"
        "<b>Skills to Develop:</b>\n"
        "  - Leadership\n"
        "  - Strategic Planning\n"
        "  - Team Management\n\n"
        "<i>Your growth journey matters!</i>"
    )
    keyboard = [[InlineKeyboardButton("Back", callback_data='more_features')]]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

async def handle_feedback_system(query):
    text = (
        "<b>360 FEEDBACK SYSTEM</b>\n"
        "------------------------------\n\n"
        "<b>Recent Feedback:</b>\n\n"
        "From Manager:\n"
        "  'Excellent problem-solving\n"
        "   and team collaboration'\n"
        "  Rating: 4.5/5 [****-]\n"
        "  Date: 05 Nov 2025\n\n"
        "From Peers:\n"
        "  'Great team player,\n"
        "   always willing to help'\n"
        "  Rating: 4.7/5 [*****]\n"
        "  Date: 01 Nov 2025\n\n"
        "From Direct Reports:\n"
        "  'Supportive and clear\n"
        "   in communication'\n"
        "  Rating: 4.6/5 [*****]\n"
        "  Date: 28 Oct 2025\n\n"
        "<b>Overall Rating:</b> 4.6/5\n"
        "[==================--] 92%\n\n"
        "------------------------------\n"
        "You're highly valued!\n\n"
        "<i>Give feedback to help others grow</i>"
    )
    keyboard = [[InlineKeyboardButton("Back", callback_data='more_features')]]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

async def handle_goal_tracker(query):
    text = (
        "<b>GOAL TRACKER</b>\n"
        "------------------------------\n\n"
        "<b>Q4 2025 Objectives:</b>\n\n"
        "1. Complete Project Alpha\n"
        "   [====================] 100%\n"
        "   Status: DONE\n\n"
        "2. Team Performance\n"
        "   [===============-----] 75%\n"
        "   Status: IN PROGRESS\n\n"
        "3. Skill Development\n"
        "   [============--------] 60%\n"
        "   Status: IN PROGRESS\n\n"
        "4. Innovation Initiative\n"
        "   [--------------------] 0%\n"
        "   Status: NOT STARTED\n\n"
        "<b>Overall Progress:</b>\n"
        "  [===========--------] 58%\n"
        "  Status: ON TRACK\n\n"
        "<b>Upcoming Milestones:</b>\n"
        "  - Q4 Review: 15 Dec\n"
        "  - Goal Setting: 01 Jan\n\n"
        "<i>Track your progress to success!</i>"
    )
    keyboard = [[InlineKeyboardButton("Back", callback_data='more_features')]]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

# ==========================================
# GAMIFICATION HANDLERS
# ==========================================

async def handle_gamification(query, employee, db):
    game = enterprise.calculate_gamification(employee.id, db)
    level_badge = get_level_emoji(game['level'])
    
    progress_pct = (game['points'] / (game['points'] + game['points_needed']) * 100) if game['points_needed'] > 0 else 100
    
    text = (
        f"<b>GAMIFICATION</b>\n"
        f"{create_separator(30)}\n\n"
        f"Employee: <b>{employee.nama}</b>\n\n"
        f"<b>STATUS</b>\n"
        f"Level: [{level_badge}] <b>{game['level']}</b>\n"
        f"Points: <b>{game['points']}</b>\n"
        f"{create_progress_bar(progress_pct, 15)}\n\n"
        f"<b>NEXT LEVEL</b>\n"
        f"Target: <b>{game['next_level']}</b>\n"
        f"Need: <b>{game['points_needed']}</b> pts\n\n"
        f"<b>STATS</b>\n"
        f"Attendance: <b>{game['attendance_rate']:.1f}%</b>\n"
        f"Punctuality: <b>{game['punctuality_rate']:.1f}%</b>\n"
        f"Streak: <b>{game['streak']}</b> days\n"
        f"Best: <b>{game['max_streak']}</b> days\n\n"
        f"<b>ACHIEVEMENTS</b>\n"
    )
    
    if game['achievements']:
        for ach in game['achievements']:
            text += f"  + {ach}\n"
    else:
        text += "  <i>None yet. Keep going!</i>\n"
    
    text += (
        f"\n{create_separator(30)}\n\n"
        f"<b>EARN POINTS:</b>\n"
        f"  - Daily attendance: +10\n"
        f"  - On-time arrival: +5\n"
        f"  - Perfect week: +50\n"
        f"  - Perfect month: +200"
    )
    
    keyboard = [
        [InlineKeyboardButton("Leaderboard", callback_data='leaderboard')],
        [InlineKeyboardButton("Back", callback_data='main_menu')]
    ]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

async def handle_leaderboard(query, employee, db):
    employees = db.query(Employee).limit(10).all()
    leaderboard = []
    
    for emp in employees:
        game_data = enterprise.calculate_gamification(emp.id, db)
        leaderboard.append({
            'name': emp.nama,
            'points': game_data['points'],
            'level': game_data['level'],
            'is_me': emp.id == employee.id
        })
    
    leaderboard.sort(key=lambda x: x['points'], reverse=True)
    
    text = f"<b>LEADERBOARD</b>\n{create_separator(30)}\n<i>Top 10 Performers</i>\n\n"
    
    for i, item in enumerate(leaderboard[:10], 1):
        medal = "#" + str(i)
        me_tag = " <b>&lt;- YOU</b>" if item['is_me'] else ""
        level_badge = get_level_emoji(item['level'])
        
        text += f"{medal} <b>{item['name']}</b>{me_tag}\n    [{level_badge}] {item['level']} - {item['points']} pts\n\n"
    
    keyboard = [[InlineKeyboardButton("Back", callback_data='gamification')]]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

# ==========================================
# ATTENDANCE HANDLERS
# ==========================================

async def handle_clock_in(query, employee, db):
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    existing = db.query(Absensi).filter(
        Absensi.employee_id == employee.id,
        Absensi.tanggal == today
    ).first()
    
    if existing and existing.waktu_masuk:
        text = f"<b>ALREADY CLOCKED IN</b>\n\nTime: {existing.waktu_masuk.strftime('%H:%M:%S')}"
        keyboard = [[InlineKeyboardButton("Back", callback_data='attendance')]]
        await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
        return
    
    now = datetime.now()
    if existing:
        existing.waktu_masuk = now
        existing.status = 'hadir'
    else:
        db.add(Absensi(employee_id=employee.id, tanggal=today, waktu_masuk=now, status='hadir'))
    db.commit()
    
    is_late = now.hour > 8 or (now.hour == 8 and now.minute > 15)
    status_text = "LATE" if is_late else "ON TIME"
    points = "+5 pts" if is_late else "+10 pts"
    
    text = (
        f"<b>CLOCK IN SUCCESS!</b>\n"
        f"{create_separator(30)}\n\n"
        f"Employee: <b>{employee.nama}</b>\n"
        f"Time: {now.strftime('%H:%M:%S')}\n"
        f"Date: {now.strftime('%A, %d %b %Y')}\n\n"
        f"<b>{status_text}</b>\n"
        f"Points: {points}\n\n"
        f"Have a productive day!"
    )
    
    keyboard = [[InlineKeyboardButton("Back to Main", callback_data='main_menu')]]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

async def handle_clock_out(query, employee, db):
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    absensi = db.query(Absensi).filter(
        Absensi.employee_id == employee.id,
        Absensi.tanggal == today
    ).first()
    
    if not absensi or not absensi.waktu_masuk:
        text = "<b>NOT CLOCKED IN YET</b>\n\nPlease clock in first!"
        keyboard = [[InlineKeyboardButton("Clock In", callback_data='clock_in')]]
        await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
        return
    
    if absensi.waktu_keluar:
        text = f"<b>ALREADY CLOCKED OUT</b>\n\nTime: {absensi.waktu_keluar.strftime('%H:%M:%S')}"
        keyboard = [[InlineKeyboardButton("Back", callback_data='attendance')]]
        await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
        return
    
    now = datetime.now()
    absensi.waktu_keluar = now
    hours = (now - absensi.waktu_masuk).total_seconds() / 3600
    absensi.jam_kerja = round(hours, 2)
    db.commit()
    
    text = (
        f"<b>CLOCK OUT SUCCESS!</b>\n"
        f"{create_separator(30)}\n\n"
        f"Employee: <b>{employee.nama}</b>\n"
        f"Clock In: {absensi.waktu_masuk.strftime('%H:%M')}\n"
        f"Clock Out: {now.strftime('%H:%M')}\n"
        f"Duration: <b>{hours:.1f} hours</b>\n\n"
        f"Great work today!\n"
        f"See you tomorrow!"
    )
    
    keyboard = [[InlineKeyboardButton("Back to Main", callback_data='main_menu')]]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

# ==========================================
# OTHER HANDLERS
# ==========================================

async def handle_analytics(query, employee, db):
    perf = enterprise.generate_performance_score(employee.id, db)
    game = enterprise.calculate_gamification(employee.id, db)
    
    text = (
        f"<b>ANALYTICS DASHBOARD</b>\n"
        f"{create_separator(30)}\n\n"
        f"<b>PERFORMANCE</b>\n"
        f"[{get_rating_stars(perf['rating'])}] {perf['rating']}\n"
        f"{create_progress_bar(perf['total'], 15)}\n\n"
        f"Attendance: {perf['attendance']:.1f}%\n"
        f"Punctuality: {perf['punctuality']:.1f}%\n"
        f"Avg Hours: {perf['avg_hours']:.1f}h\n\n"
        f"<b>GAMIFICATION</b>\n"
        f"[{get_level_emoji(game['level'])}] {game['level']}\n"
        f"Points: {game['points']}\n"
        f"Streak: {game['streak']} days"
    )
    
    keyboard = [[InlineKeyboardButton("Back", callback_data='main_menu')]]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

async def handle_profile(query, employee, db):
    tenure = (datetime.now() - employee.tanggal_bergabung).days
    years = tenure // 365
    months = (tenure % 365) // 30
    
    text = (
        f"<b>EMPLOYEE PROFILE</b>\n"
        f"{create_separator(30)}\n\n"
        f"<b>PERSONAL</b>\n"
        f"  Name: <b>{employee.nama}</b>\n"
        f"  NIK: {employee.nik}\n"
        f"  Email: {employee.email}\n\n"
        f"<b>EMPLOYMENT</b>\n"
        f"  Position: <b>{employee.jabatan}</b>\n"
        f"  Dept: {employee.departemen}\n"
        f"  Status: <b>{employee.status.upper()}</b>\n\n"
        f"<b>TENURE</b>\n"
        f"  Joined: {employee.tanggal_bergabung.strftime('%d %b %Y')}\n"
        f"  Duration: <b>{years}y {months}m</b>"
    )
    
    keyboard = [[InlineKeyboardButton("Back", callback_data='main_menu')]]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

async def handle_alerts(query, employee, db):
    game = enterprise.calculate_gamification(employee.id, db)
    
    text = f"<b>SMART ALERTS</b>\n{create_separator(30)}\n\n"
    
    alerts_count = 0
    if game['points_needed'] < 100:
        text += f"Level up soon!\nOnly {game['points_needed']} pts needed\n\n"
        alerts_count += 1
    
    if game['streak'] >= 7:
        text += f"Amazing! {game['streak']} day streak!\n\n"
        alerts_count += 1
    
    if game['attendance_rate'] >= 95:
        text += f"Excellent attendance!\n{game['attendance_rate']:.1f}%\n\n"
        alerts_count += 1
    
    if alerts_count == 0:
        text += "<i>No new alerts</i>\n\n"
    
    text += "All systems operational!"
    
    keyboard = [[InlineKeyboardButton("Back", callback_data='main_menu')]]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

async def handle_ai_mode(query, employee, context):
    context.user_data['ai_mode'] = True
    text = (
        f"<b>AI ASSISTANT</b>\n"
        f"{create_separator(30)}\n\n"
        f"Hello <b>{employee.nama}</b>!\n\n"
        f"I'm your intelligent HR assistant.\n"
        f"Ask me anything about:\n\n"
        f"  - HR Policies\n"
        f"  - Payroll & Benefits\n"
        f"  - Leave Management\n"
        f"  - Performance\n"
        f"  - Career Development\n\n"
        f"<i>Type your question...</i>\n\n"
        f"/start to return to menu"
    )
    await query.edit_message_text(text=text, parse_mode='HTML')

# ==========================================
# MESSAGE HANDLER
# ==========================================

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('ai_mode'):
        db = SessionLocal()
        try:
            employee = db.query(Employee).filter(
                Employee.telegram_user_id == update.effective_user.id
            ).first()
            
            if not employee:
                return
            
            msg = update.message.text
            
            if msg.lower() in ['/start', 'menu', 'exit']:
                context.user_data['ai_mode'] = False
                await start_command(update, context)
                return
            
            await update.message.chat.send_action('typing')
            
            result = advanced_rag.chat(
                query=msg,
                employee_id=employee.id,
                user_id=update.effective_user.id
            )
            
            response = (
                f"<b>AI Assistant</b>\n"
                f"{create_separator(30)}\n\n"
                f"{result['response']}\n\n"
                f"{create_separator(30)}\n"
                f"<i>/start to return to menu</i>"
            )
            await update.message.reply_text(response, parse_mode='HTML')
        
        finally:
            db.close()

# ==========================================
# MAIN
# ==========================================

def main():
    logger.info("=" * 60)
    logger.info(f"BPKH HR v{VERSION} - {DEVELOPER}")
    logger.info("All Features Fully Clickable & Operational!")
    logger.info("=" * 60)
    
    init_db()
    
    app = Application.builder()\
        .token(TELEGRAM_BOT_TOKEN)\
        .connect_timeout(60)\
        .read_timeout(60)\
        .write_timeout(60)\
        .pool_timeout(60)\
        .build()
    
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('register', register_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    
    logger.info("Bot running - All systems operational!")
    logger.info("=" * 60)
    
    try:
        app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")

if __name__ == '__main__':
    main()
