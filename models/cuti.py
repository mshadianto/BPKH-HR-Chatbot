# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Cuti(Base):
    __tablename__ = 'cuti'
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    jenis_cuti = Column(String(50))
    tanggal_mulai = Column(DateTime)
    tanggal_selesai = Column(DateTime)
    jumlah_hari = Column(Integer)
    alasan = Column(Text)
    status = Column(String(20), default='pending')
    approved_by = Column(Integer, nullable=True)
    approved_at = Column(DateTime, nullable=True)
    catatan = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    employee = relationship('Employee', back_populates='cuti')
