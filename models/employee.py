"""Employee model."""
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Employee(Base):
    __tablename__ = 'employees'
    
    id = Column(Integer, primary_key=True)
    telegram_user_id = Column(Integer, unique=True, index=True)
    nik = Column(String(20), unique=True, index=True)
    nama = Column(String(100))
    email = Column(String(100))
    jabatan = Column(String(100))
    departemen = Column(String(100))
    tanggal_bergabung = Column(DateTime)
    gaji_pokok = Column(Float)
    status = Column(String(20), default='aktif')
    created_at = Column(DateTime, default=datetime.now)
    
    # Relationships (harus sama dengan back_populates di model lain)
    cuti = relationship('Cuti', back_populates='employee', cascade='all, delete-orphan')
    absensi = relationship('Absensi', back_populates='employee', cascade='all, delete-orphan')
    payroll = relationship('Payroll', back_populates='employee', cascade='all, delete-orphan')
