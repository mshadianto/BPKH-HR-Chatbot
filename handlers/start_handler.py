"""Handler untuk command /start dan menu utama."""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from models import SessionLocal, Employee

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db = SessionLocal()
    try:
        employee = db.query(Employee).filter(Employee.telegram_user_id == user.id).first()
        if not employee:
            await update.message.reply_text("Akun belum terdaftar. Hubungi admin.")
            return
        await show_main_menu(update, context, employee)
    finally:
        db.close()

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, employee=None):
    keyboard = [
        [InlineKeyboardButton("Payroll", callback_data='menu_payroll'), InlineKeyboardButton("Cuti", callback_data='menu_cuti')],
        [InlineKeyboardButton("Absensi", callback_data='menu_absensi'), InlineKeyboardButton("Info", callback_data='menu_employee')],
        [InlineKeyboardButton("AI", callback_data='menu_ai')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = f"SISTEM HR\n\nHalo {employee.nama if employee else 'User'}!" if employee else "SISTEM HR"
    if update.callback_query:
        await update.callback_query.edit_message_text(text=text, reply_markup=reply_markup)
    else:
        await update.message.reply_text(text=text, reply_markup=reply_markup)
