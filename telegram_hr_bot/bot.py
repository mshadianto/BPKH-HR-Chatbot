import os
import logging
from datetime import datetime, date
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    filters,
    ContextTypes
)
from database import get_session, Employee, Cuti, Absensi, Payroll, KnowledgeBase, init_db
from rag_engine import RAGEngine, DEFAULT_KNOWLEDGE

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize RAG Engine
rag_engine = RAGEngine()

# Conversation states
AWAITING_QUESTION, AWAITING_CUTI_TYPE, AWAITING_CUTI_START, AWAITING_CUTI_END, AWAITING_CUTI_REASON = range(5)
AWAITING_ABSEN_TYPE = 10

class SDMBot:
    def __init__(self):
        self.session = get_session()
        
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start command - show main menu"""
        user = update.effective_user
        telegram_id = str(user.id)
        
        # Check if user is registered
        employee = self.session.query(Employee).filter_by(telegram_id=telegram_id).first()
        
        if not employee:
            await update.message.reply_text(
                f"👋 Halo {user.first_name}!\n\n"
                "Anda belum terdaftar dalam sistem SDM.\n"
                "Silakan hubungi HRD untuk registrasi akun Anda.\n\n"
                "Gunakan /register untuk mendaftar (Admin only)"
            )
            return
        
        keyboard = [
            [InlineKeyboardButton("1️⃣ Payroll", callback_data='menu_payroll')],
            [InlineKeyboardButton("2️⃣ Cuti", callback_data='menu_cuti')],
            [InlineKeyboardButton("3️⃣ Absensi", callback_data='menu_absensi')],
            [InlineKeyboardButton("4️⃣ Info Karyawan", callback_data='menu_info')],
            [InlineKeyboardButton("5️⃣ BPJS & Benefit", callback_data='menu_bpjs')],
            [InlineKeyboardButton("6️⃣ Kebijakan HR", callback_data='menu_kebijakan')],
            [InlineKeyboardButton("💬 Tanya AI", callback_data='menu_ai')],
            [InlineKeyboardButton("❓ Help", callback_data='menu_help')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        welcome_text = f"""
🏢 *Selamat Datang di Bot SDM*

Halo *{employee.nama}*! 👋

Pilih menu yang Anda butuhkan:

1️⃣ *Payroll* - Info gaji dan slip gaji
2️⃣ *Cuti* - Ajukan dan cek status cuti
3️⃣ *Absensi* - Absen & laporan kehadiran
4️⃣ *Info Karyawan* - Data pribadi Anda
5️⃣ *BPJS & Benefit* - Info tunjangan
6️⃣ *Kebijakan HR* - Aturan perusahaan
💬 *Tanya AI* - Tanya apapun ke AI SDM
❓ *Help* - Bantuan penggunaan bot

_Ketik /start kapan saja untuk kembali ke menu utama_
        """
        
        await update.message.reply_text(
            welcome_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button callbacks"""
        query = update.callback_query
        await query.answer()
        
        telegram_id = str(query.from_user.id)
        employee = self.session.query(Employee).filter_by(telegram_id=telegram_id).first()
        
        if not employee and query.data != 'menu_help':
            await query.edit_message_text("❌ Anda belum terdaftar. Hubungi HRD untuk registrasi.")
            return
        
        # Main Menu Handlers
        if query.data == 'menu_payroll':
            await self.show_payroll_menu(query, employee)
        elif query.data == 'menu_cuti':
            await self.show_cuti_menu(query, employee)
        elif query.data == 'menu_absensi':
            await self.show_absensi_menu(query, employee)
        elif query.data == 'menu_info':
            await self.show_info_karyawan(query, employee)
        elif query.data == 'menu_bpjs':
            await self.show_bpjs_info(query, employee)
        elif query.data == 'menu_kebijakan':
            await self.show_kebijakan_menu(query)
        elif query.data == 'menu_ai':
            await self.show_ai_menu(query)
        elif query.data == 'menu_help':
            await self.show_help(query)
        elif query.data == 'back_main':
            await self.show_main_menu(query, employee)
        
        # Payroll sub-menu
        elif query.data == 'payroll_current':
            await self.show_current_payroll(query, employee)
        elif query.data == 'payroll_history':
            await self.show_payroll_history(query, employee)
        elif query.data == 'payroll_slip':
            await self.generate_slip_gaji(query, employee)
        
        # Cuti sub-menu
        elif query.data == 'cuti_saldo':
            await self.show_saldo_cuti(query, employee)
        elif query.data == 'cuti_ajukan':
            await self.start_cuti_process(query, context)
        elif query.data == 'cuti_status':
            await self.show_status_cuti(query, employee)
        elif query.data == 'cuti_history':
            await self.show_history_cuti(query, employee)
        
        # Absensi sub-menu
        elif query.data == 'absen_masuk':
            await self.absen_masuk(query, employee)
        elif query.data == 'absen_pulang':
            await self.absen_pulang(query, employee)
        elif query.data == 'absen_history':
            await self.show_absensi_history(query, employee)
        elif query.data == 'absen_summary':
            await self.show_absensi_summary(query, employee)
    
    async def show_main_menu(self, query, employee):
        """Show main menu"""
        keyboard = [
            [InlineKeyboardButton("1️⃣ Payroll", callback_data='menu_payroll')],
            [InlineKeyboardButton("2️⃣ Cuti", callback_data='menu_cuti')],
            [InlineKeyboardButton("3️⃣ Absensi", callback_data='menu_absensi')],
            [InlineKeyboardButton("4️⃣ Info Karyawan", callback_data='menu_info')],
            [InlineKeyboardButton("5️⃣ BPJS & Benefit", callback_data='menu_bpjs')],
            [InlineKeyboardButton("6️⃣ Kebijakan HR", callback_data='menu_kebijakan')],
            [InlineKeyboardButton("💬 Tanya AI", callback_data='menu_ai')],
            [InlineKeyboardButton("❓ Help", callback_data='menu_help')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            f"🏢 *Menu Utama*\n\nHalo {employee.nama}!\nPilih menu yang Anda butuhkan:",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def show_payroll_menu(self, query, employee):
        """Show payroll submenu"""
        keyboard = [
            [InlineKeyboardButton("💰 Gaji Bulan Ini", callback_data='payroll_current')],
            [InlineKeyboardButton("📊 Riwayat Gaji", callback_data='payroll_history')],
            [InlineKeyboardButton("🧾 Download Slip Gaji", callback_data='payroll_slip')],
            [InlineKeyboardButton("🔙 Kembali", callback_data='back_main')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "💰 *Menu Payroll*\n\nPilih informasi yang ingin Anda lihat:",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def show_current_payroll(self, query, employee):
        """Show current month payroll"""
        current_period = datetime.now().strftime('%Y-%m')
        payroll = self.session.query(Payroll).filter_by(
            employee_id=employee.id,
            periode=current_period
        ).first()
        
        if not payroll:
            text = f"""
💰 *Informasi Gaji - {current_period}*

❌ Data gaji bulan ini belum tersedia.
Gaji biasanya diproses tanggal 20-25 setiap bulan.

_Hubungi HRD untuk informasi lebih lanjut._
            """
        else:
            text = f"""
💰 *Slip Gaji - {payroll.periode}*

👤 *Karyawan:* {employee.nama}
🆔 *NIP:* {employee.nip}
💼 *Jabatan:* {employee.jabatan}

*PENGHASILAN:*
• Gaji Pokok: Rp {payroll.gaji_pokok:,.0f}
• Tunjangan: Rp {payroll.tunjangan:,.0f}
• Bonus: Rp {payroll.bonus:,.0f}

*POTONGAN:*
• Potongan: Rp {payroll.potongan:,.0f}

*TOTAL GAJI:* Rp {payroll.total_gaji:,.0f}

📅 Tanggal Bayar: {payroll.tanggal_bayar if payroll.tanggal_bayar else 'Belum ditentukan'}
📌 Status: {payroll.status}
            """
        
        keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data='menu_payroll')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def show_payroll_history(self, query, employee):
        """Show payroll history"""
        payrolls = self.session.query(Payroll).filter_by(
            employee_id=employee.id
        ).order_by(Payroll.periode.desc()).limit(6).all()
        
        if not payrolls:
            text = "📊 *Riwayat Gaji*\n\n❌ Belum ada data riwayat gaji."
        else:
            text = "📊 *Riwayat Gaji (6 Bulan Terakhir)*\n\n"
            for p in payrolls:
                text += f"• {p.periode}: Rp {p.total_gaji:,.0f} ({p.status})\n"
        
        keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data='menu_payroll')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def generate_slip_gaji(self, query, employee):
        """Generate salary slip"""
        current_period = datetime.now().strftime('%Y-%m')
        
        text = f"""
🧾 *Download Slip Gaji*

Untuk mendownload slip gaji resmi, silakan:
1. Akses sistem HRIS: https://hris.perusahaan.com
2. Login dengan akun Anda
3. Menu Payroll > Download Slip Gaji
4. Pilih periode: {current_period}

_Atau hubungi HRD untuk bantuan._
        """
        
        keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data='menu_payroll')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def show_cuti_menu(self, query, employee):
        """Show cuti submenu"""
        keyboard = [
            [InlineKeyboardButton("📅 Saldo Cuti", callback_data='cuti_saldo')],
            [InlineKeyboardButton("✍️ Ajukan Cuti", callback_data='cuti_ajukan')],
            [InlineKeyboardButton("📋 Status Pengajuan", callback_data='cuti_status')],
            [InlineKeyboardButton("📊 Riwayat Cuti", callback_data='cuti_history')],
            [InlineKeyboardButton("🔙 Kembali", callback_data='back_main')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "🏖️ *Menu Cuti*\n\nPilih menu cuti:",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def show_saldo_cuti(self, query, employee):
        """Show cuti balance"""
        # Calculate used leave days
        current_year = datetime.now().year
        used_days = self.session.query(Cuti).filter(
            Cuti.employee_id == employee.id,
            Cuti.status == 'Approved',
            Cuti.tanggal_mulai >= date(current_year, 1, 1)
        ).count()
        
        total_cuti = 12
        remaining = total_cuti - used_days
        
        text = f"""
📅 *Saldo Cuti Tahun {current_year}*

👤 Nama: {employee.nama}

📊 *Status Cuti:*
• Total Hak Cuti: {total_cuti} hari
• Sudah Digunakan: {used_days} hari
• Sisa Cuti: {remaining} hari

_Cuti tahunan berlaku dari Jan - Des {current_year}_
_Sisa cuti tidak dapat diakumulasikan ke tahun berikutnya_
        """
        
        keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data='menu_cuti')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def start_cuti_process(self, query, context):
        """Start leave application process"""
        await query.edit_message_text(
            "✍️ *Pengajuan Cuti*\n\n"
            "Silakan pilih jenis cuti:\n\n"
            "1. Cuti Tahunan\n"
            "2. Cuti Sakit\n"
            "3. Cuti Penting (Pernikahan, dll)\n\n"
            "Ketik nomor pilihan (1/2/3):",
            parse_mode='Markdown'
        )
        return AWAITING_CUTI_TYPE
    
    async def show_status_cuti(self, query, employee):
        """Show leave application status"""
        pending_cuti = self.session.query(Cuti).filter(
            Cuti.employee_id == employee.id,
            Cuti.status == 'Pending'
        ).all()
        
        if not pending_cuti:
            text = "📋 *Status Pengajuan Cuti*\n\n✅ Tidak ada pengajuan cuti yang pending."
        else:
            text = "📋 *Status Pengajuan Cuti*\n\n"
            for c in pending_cuti:
                text += f"""
• *Jenis:* {c.jenis_cuti}
  *Tanggal:* {c.tanggal_mulai} s/d {c.tanggal_selesai}
  *Status:* ⏳ {c.status}
  *Durasi:* {c.jumlah_hari} hari

"""
        
        keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data='menu_cuti')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def show_history_cuti(self, query, employee):
        """Show leave history"""
        cuti_list = self.session.query(Cuti).filter(
            Cuti.employee_id == employee.id
        ).order_by(Cuti.created_at.desc()).limit(10).all()
        
        if not cuti_list:
            text = "📊 *Riwayat Cuti*\n\n❌ Belum ada riwayat cuti."
        else:
            text = "📊 *Riwayat Cuti*\n\n"
            for c in cuti_list:
                status_icon = "✅" if c.status == "Approved" else "❌" if c.status == "Rejected" else "⏳"
                text += f"• {c.tanggal_mulai}: {c.jenis_cuti} - {status_icon} {c.status}\n"
        
        keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data='menu_cuti')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def show_absensi_menu(self, query, employee):
        """Show attendance submenu"""
        keyboard = [
            [InlineKeyboardButton("✅ Absen Masuk", callback_data='absen_masuk')],
            [InlineKeyboardButton("🏃 Absen Pulang", callback_data='absen_pulang')],
            [InlineKeyboardButton("📊 Riwayat Absensi", callback_data='absen_history')],
            [InlineKeyboardButton("📈 Ringkasan Bulan Ini", callback_data='absen_summary')],
            [InlineKeyboardButton("🔙 Kembali", callback_data='back_main')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "📋 *Menu Absensi*\n\nPilih menu absensi:",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def absen_masuk(self, query, employee):
        """Clock in"""
        today = date.today()
        existing = self.session.query(Absensi).filter(
            Absensi.employee_id == employee.id,
            Absensi.tanggal == today
        ).first()
        
        if existing and existing.jam_masuk:
            text = f"❌ Anda sudah absen masuk hari ini pada jam {existing.jam_masuk}"
        else:
            now = datetime.now()
            jam_masuk = now.strftime('%H:%M:%S')
            
            if existing:
                existing.jam_masuk = jam_masuk
                existing.status = 'Hadir'
            else:
                absensi = Absensi(
                    employee_id=employee.id,
                    tanggal=today,
                    jam_masuk=jam_masuk,
                    status='Hadir'
                )
                self.session.add(absensi)
            
            self.session.commit()
            
            # Check if late
            jam_kerja = now.replace(hour=8, minute=15, second=0)
            status = "Terlambat ⚠️" if now > jam_kerja else "Tepat Waktu ✅"
            
            text = f"""
✅ *Absen Masuk Berhasil!*

📅 Tanggal: {today.strftime('%d/%m/%Y')}
⏰ Jam Masuk: {jam_masuk}
📍 Status: {status}

Selamat bekerja, {employee.nama}! 💪
            """
        
        keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data='menu_absensi')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def absen_pulang(self, query, employee):
        """Clock out"""
        today = date.today()
        absensi = self.session.query(Absensi).filter(
            Absensi.employee_id == employee.id,
            Absensi.tanggal == today
        ).first()
        
        if not absensi or not absensi.jam_masuk:
            text = "❌ Anda belum absen masuk hari ini."
        elif absensi.jam_keluar:
            text = f"❌ Anda sudah absen pulang pada jam {absensi.jam_keluar}"
        else:
            jam_keluar = datetime.now().strftime('%H:%M:%S')
            absensi.jam_keluar = jam_keluar
            self.session.commit()
            
            text = f"""
🏃 *Absen Pulang Berhasil!*

📅 Tanggal: {today.strftime('%d/%m/%Y')}
⏰ Jam Masuk: {absensi.jam_masuk}
⏰ Jam Keluar: {jam_keluar}

Terima kasih atas kerja keras Anda hari ini! 🙏
Sampai jumpa besok!
            """
        
        keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data='menu_absensi')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def show_absensi_history(self, query, employee):
        """Show attendance history"""
        absensi_list = self.session.query(Absensi).filter(
            Absensi.employee_id == employee.id
        ).order_by(Absensi.tanggal.desc()).limit(10).all()
        
        if not absensi_list:
            text = "📊 *Riwayat Absensi*\n\n❌ Belum ada data absensi."
        else:
            text = "📊 *Riwayat Absensi (10 Hari Terakhir)*\n\n"
            for a in absensi_list:
                masuk = a.jam_masuk if a.jam_masuk else "-"
                keluar = a.jam_keluar if a.jam_keluar else "-"
                text += f"• {a.tanggal}: {masuk} - {keluar} ({a.status})\n"
        
        keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data='menu_absensi')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def show_absensi_summary(self, query, employee):
        """Show attendance summary for current month"""
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        absensi_list = self.session.query(Absensi).filter(
            Absensi.employee_id == employee.id,
            Absensi.tanggal >= date(current_year, current_month, 1)
        ).all()
        
        hadir = len([a for a in absensi_list if a.status == 'Hadir'])
        izin = len([a for a in absensi_list if a.status == 'Izin'])
        sakit = len([a for a in absensi_list if a.status == 'Sakit'])
        alfa = len([a for a in absensi_list if a.status == 'Alfa'])
        
        text = f"""
📈 *Ringkasan Absensi Bulan Ini*

📅 Periode: {datetime.now().strftime('%B %Y')}

📊 *Status Kehadiran:*
• Hadir: {hadir} hari ✅
• Izin: {izin} hari 📝
• Sakit: {sakit} hari 🏥
• Alfa: {alfa} hari ❌

Total: {len(absensi_list)} hari
        """
        
        keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data='menu_absensi')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def show_info_karyawan(self, query, employee):
        """Show employee information"""
        text = f"""
👤 *Informasi Karyawan*

*DATA PRIBADI:*
• Nama: {employee.nama}
• NIP: {employee.nip}
• Email: {employee.email}
• Jabatan: {employee.jabatan}
• Departemen: {employee.departemen}

*DATA KEPEGAWAIAN:*
• Tanggal Masuk: {employee.tanggal_masuk}
• Status: {'Aktif ✅' if employee.is_active else 'Non-Aktif ❌'}

_Untuk update data, hubungi HRD_
        """
        
        keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data='back_main')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def show_bpjs_info(self, query, employee):
        """Show BPJS and benefits information"""
        text = """
🏥 *BPJS & Benefit*

*BPJS KESEHATAN:*
• Kelas: 1
• Tanggungan: Max 3 orang
• Coverage: Rawat inap, jalan, obat

*BPJS KETENAGAKERJAAN:*
• JHT (Jaminan Hari Tua)
• JP (Jaminan Pensiun)
• JKK (Jaminan Kecelakaan Kerja)
• JKM (Jaminan Kematian)

*BENEFIT LAINNYA:*
• Tunjangan Transport
• Tunjangan Makan
• THR (Tunjangan Hari Raya)
• Bonus Kinerja (sesuai KPI)

_Detail iuran ada di slip gaji bulanan_
        """
        
        keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data='back_main')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def show_kebijakan_menu(self, query):
        """Show company policy"""
        text = """
📋 *Kebijakan Perusahaan*

*JAM KERJA:*
• Senin-Jumat: 08:00 - 17:00 WIB
• Istirahat: 12:00 - 13:00 WIB
• Toleransi: 15 menit

*WORK FROM HOME (WFH):*
• Max 2 hari/minggu
• Harus approval atasan
• Wajib absen & online

*LEMBUR:*
• Persetujuan atasan
• Hari kerja: 1.5x
• Hari libur: 2x
• Min 1 jam

*DRESS CODE:*
• Senin-Kamis: Formal
• Jumat: Batik/Smart Casual
• WFH: Bebas rapi

Untuk detail kebijakan, tanya AI atau hubungi HRD!
        """
        
        keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data='back_main')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def show_ai_menu(self, query):
        """Show AI assistant menu"""
        text = """
💬 *Tanya AI SDM*

Tanyakan apapun tentang:
• Kebijakan perusahaan
• Prosedur payroll & cuti
• Aturan absensi & lembur
• BPJS dan benefit
• Dan lainnya!

Contoh pertanyaan:
"Bagaimana cara mengajukan cuti?"
"Kapan gaji dibayarkan?"
"Apa saja jenis cuti yang ada?"

Silakan ketik pertanyaan Anda...
        """
        
        keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data='back_main')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
        return AWAITING_QUESTION
    
    async def handle_ai_question(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle AI questions using RAG"""
        question = update.message.text
        
        await update.message.reply_text("🤔 Sedang mencari jawaban...")
        
        try:
            answer = rag_engine.query(question)
            await update.message.reply_text(
                f"💬 *Jawaban AI:*\n\n{answer}\n\n_Ketik /start untuk kembali ke menu_",
                parse_mode='Markdown'
            )
        except Exception as e:
            await update.message.reply_text(
                f"❌ Maaf, terjadi kesalahan: {str(e)}\n\nKetik /start untuk kembali ke menu."
            )
        
        return ConversationHandler.END
    
    async def show_help(self, query):
        """Show help information"""
        text = """
❓ *Bantuan Penggunaan Bot*

*CARA MENGGUNAKAN:*
1. Ketik /start untuk membuka menu
2. Pilih menu sesuai kebutuhan
3. Ikuti instruksi yang diberikan

*FITUR UTAMA:*
• 💰 Payroll - Cek gaji & slip
• 🏖️ Cuti - Ajukan & tracking
• 📋 Absensi - Clock in/out
• 💬 AI - Tanya apapun

*KONTAK SUPPORT:*
• Email: hrd@perusahaan.com
• Telp: 021-12345678
• WhatsApp: 0812-3456-7890

*TIPS:*
- Gunakan menu AI untuk pertanyaan umum
- Ajukan cuti minimal H-3
- Absen setiap hari kerja
- Cek payroll setiap akhir bulan

Ketik /start kapan saja untuk kembali!
        """
        
        keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data='back_main')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

def main():
    """Start the bot"""
    # Initialize database
    init_db()
    
    # Initialize RAG with default knowledge
    print("Initializing RAG Engine...")
    rag_engine.initialize_knowledge_base(DEFAULT_KNOWLEDGE)
    print("RAG Engine ready!")
    
    # Create bot instance
    bot = SDMBot()
    
    # Create application
    application = Application.builder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", bot.start))
    application.add_handler(CallbackQueryHandler(bot.button_handler))
    
    # AI conversation handler
    ai_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(bot.show_ai_menu, pattern='^menu_ai$')],
        states={
            AWAITING_QUESTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_ai_question)]
        },
        fallbacks=[CommandHandler('start', bot.start)]
    )
    application.add_handler(ai_conv_handler)
    
    # Start the bot
    print("Bot is running...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()