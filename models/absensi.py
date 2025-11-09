# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, DateTime, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Absensi(Base):
    __tablename__ = 'absensi'
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    tanggal = Column(DateTime)
    waktu_masuk = Column(DateTime, nullable=True)
    waktu_keluar = Column(DateTime, nullable=True)
    status = Column(String(20))
    lokasi_masuk = Column(String(200), nullable=True)
    lokasi_keluar = Column(String(200), nullable=True)
    jam_kerja = Column(Float, default=0.0)
    catatan = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    employee = relationship('Employee', back_populates='absensi')
