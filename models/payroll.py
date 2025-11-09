# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, Float, DateTime, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Payroll(Base):
    __tablename__ = 'payroll'
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    periode = Column(String(7))
    gaji_pokok = Column(Float)
    tunjangan = Column(Float, default=0.0)
    bonus = Column(Float, default=0.0)
    potongan = Column(Float, default=0.0)
    total_gaji = Column(Float)
    status = Column(String(20), default='draft')
    tanggal_dibayar = Column(DateTime, nullable=True)
    keterangan = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    employee = relationship('Employee', back_populates='payroll')
