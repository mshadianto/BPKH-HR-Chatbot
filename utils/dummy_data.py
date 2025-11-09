"""Generator untuk dummy data testing."""
from models import SessionLocal, Employee, Cuti, Absensi, Payroll, KnowledgeBase
from datetime import datetime, timedelta
import random

FIRST_NAMES = ['Ahmad', 'Siti', 'Budi', 'Dewi', 'Rudi', 'Sri', 'Agus', 'Rina', 'Eko', 'Maya']
LAST_NAMES = ['Santoso', 'Wijaya', 'Setiawan', 'Gunawan', 'Hidayat', 'Nugroho', 'Pratama', 'Firmansyah']
JABATAN = ['Staff Keuangan', 'Staff Administrasi', 'Supervisor', 'Manager', 'Analyst', 'Specialist']
DEPARTEMEN = ['Keuangan Haji', 'Investasi', 'Administrasi', 'IT', 'SDM', 'Umum']

def generate_employees(count=20):
    db = SessionLocal()
    try:
        db.query(Employee).delete()
        db.commit()
        
        for i in range(count):
            nama = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
            nik = f"BPKH{2024}{str(i+1).zfill(3)}"
            
            employee = Employee(
                telegram_user_id=100000 + i,
                nik=nik,
                nama=nama,
                email=f"{nama.lower().replace(' ', '.')}@bpkh.go.id",
                jabatan=random.choice(JABATAN),
                departemen=random.choice(DEPARTEMEN),
                tanggal_bergabung=datetime.now() - timedelta(days=random.randint(365, 1825)),
                gaji_pokok=random.choice([8000000, 10000000, 12000000, 15000000, 18000000]),
                status='aktif'
            )
            db.add(employee)
        
        db.commit()
        print(f"OK {count} karyawan BPKH berhasil dibuat!")
    finally:
        db.close()

def generate_payroll(months=3):
    db = SessionLocal()
    try:
        db.query(Payroll).delete()
        db.commit()
        
        employees = db.query(Employee).all()
        
        for month in range(months):
            periode_date = datetime.now() - timedelta(days=30*month)
            periode = periode_date.strftime('%Y-%m')
            
            for emp in employees:
                tunjangan = emp.gaji_pokok * 0.3
                bonus = emp.gaji_pokok * random.choice([0, 0.1, 0.2])
                potongan = random.choice([0, 100000, 200000])
                total = emp.gaji_pokok + tunjangan + bonus - potongan
                
                payroll = Payroll(
                    employee_id=emp.id,
                    periode=periode,
                    gaji_pokok=emp.gaji_pokok,
                    tunjangan=tunjangan,
                    bonus=bonus,
                    potongan=potongan,
                    total_gaji=total,
                    status='paid',
                    tanggal_dibayar=periode_date + timedelta(days=25)
                )
                db.add(payroll)
        
        db.commit()
        print(f"OK Payroll untuk {months} bulan berhasil dibuat!")
    finally:
        db.close()

def generate_cuti():
    db = SessionLocal()
    try:
        db.query(Cuti).delete()
        db.commit()
        
        employees = db.query(Employee).all()
        
        for emp in random.sample(employees, min(10, len(employees))):
            for i in range(random.randint(1, 3)):
                start = datetime.now() + timedelta(days=random.randint(-60, 30))
                days = random.randint(2, 7)
                
                cuti = Cuti(
                    employee_id=emp.id,
                    jenis_cuti=random.choice(['tahunan', 'sakit', 'cuti besar']),
                    tanggal_mulai=start,
                    tanggal_selesai=start + timedelta(days=days),
                    jumlah_hari=days,
                    alasan='Keperluan pribadi',
                    status=random.choice(['pending', 'approved', 'approved']),
                    created_at=start - timedelta(days=7)
                )
                db.add(cuti)
        
        db.commit()
        print("OK Data cuti berhasil dibuat!")
    finally:
        db.close()

def generate_absensi():
    db = SessionLocal()
    try:
        db.query(Absensi).delete()
        db.commit()
        
        employees = db.query(Employee).all()
        
        for day in range(7):
            date = datetime.now() - timedelta(days=day)
            if date.weekday() < 5:
                for emp in employees:
                    if random.random() > 0.1:
                        waktu_masuk = date.replace(hour=8, minute=random.randint(0, 30))
                        waktu_keluar = date.replace(hour=17, minute=random.randint(0, 30))
                        
                        absensi = Absensi(
                            employee_id=emp.id,
                            tanggal=date,
                            waktu_masuk=waktu_masuk,
                            waktu_keluar=waktu_keluar,
                            status='hadir',
                            jam_kerja=8.5
                        )
                        db.add(absensi)
        
        db.commit()
        print("OK Data absensi berhasil dibuat!")
    finally:
        db.close()

def generate_knowledge_base():
    db = SessionLocal()
    try:
        db.query(KnowledgeBase).delete()
        db.commit()
        
        kb_data = [
            {
                'kategori': 'cuti',
                'judul': 'Cara Mengajukan Cuti',
                'konten': 'Untuk mengajukan cuti, gunakan menu Cuti di bot, pilih Ajukan Cuti, lalu isi tanggal dan alasan.',
                'tags': 'cuti,permohonan,pengajuan'
            },
            {
                'kategori': 'payroll',
                'judul': 'Jadwal Pembayaran Gaji',
                'konten': 'Gaji BPKH dibayarkan setiap tanggal 1 bulan berikutnya. Slip gaji dapat diunduh melalui bot.',
                'tags': 'gaji,payroll,pembayaran'
            },
        ]
        
        for data in kb_data:
            kb = KnowledgeBase(**data)
            db.add(kb)
        
        db.commit()
        print("OK Knowledge base BPKH berhasil dibuat!")
    finally:
        db.close()

if __name__ == '__main__':
    print("Membuat dummy data BPKH...")
    print("")
    generate_employees(20)
    generate_payroll(3)
    generate_cuti()
    generate_absensi()
    generate_knowledge_base()
    print("")
    print("SELESAI! Semua dummy data berhasil dibuat!")
