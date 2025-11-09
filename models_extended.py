"""Extended enterprise models."""
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from models import Base
from datetime import datetime

class LeaveBalance(Base):
    """Leave balance tracking."""
    __tablename__ = 'leave_balance'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    year = Column(Integer, nullable=False)
    annual_total = Column(Integer, default=12)
    annual_used = Column(Integer, default=0)
    sick_total = Column(Integer, default=12)
    sick_used = Column(Integer, default=0)
    updated_at = Column(DateTime, default=datetime.now)

class PerformanceReview(Base):
    """Performance review system."""
    __tablename__ = 'performance_reviews'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    reviewer_id = Column(Integer, ForeignKey('employees.id'))
    period = Column(String(20))
    overall_rating = Column(Float)
    technical_skills = Column(Float)
    communication = Column(Float)
    teamwork = Column(Float)
    leadership = Column(Float)
    strengths = Column(Text)
    improvements = Column(Text)
    goals_next_period = Column(Text)
    comments = Column(Text)
    status = Column(String(20), default='draft')
    created_at = Column(DateTime, default=datetime.now)

class Overtime(Base):
    """Overtime tracking and calculation."""
    __tablename__ = 'overtime'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    date = Column(DateTime, nullable=False)
    hours = Column(Float, nullable=False)
    reason = Column(Text)
    rate_multiplier = Column(Float, default=1.5)
    amount_calculated = Column(Float)
    status = Column(String(20), default='pending')
    approved_by = Column(Integer, ForeignKey('employees.id'))
    approved_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now)

class Notification(Base):
    """Push notification system."""
    __tablename__ = 'notifications'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    title = Column(String(200))
    message = Column(Text)
    notification_type = Column(String(50))
    priority = Column(String(20), default='normal')
    is_read = Column(Boolean, default=False)
    action_url = Column(String(500))
    metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.now)
    read_at = Column(DateTime)

class Document(Base):
    """Document management."""
    __tablename__ = 'documents'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    document_type = Column(String(50))
    title = Column(String(200))
    description = Column(Text)
    file_path = Column(String(500))
    file_size = Column(Integer)
    mime_type = Column(String(100))
    uploaded_by = Column(Integer, ForeignKey('employees.id'))
    uploaded_at = Column(DateTime, default=datetime.now)
    expires_at = Column(DateTime)
    is_verified = Column(Boolean, default=False)

class AuditLog(Base):
    """Audit trail for all actions."""
    __tablename__ = 'audit_logs'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    action = Column(String(100))
    entity_type = Column(String(50))
    entity_id = Column(Integer)
    old_values = Column(JSON)
    new_values = Column(JSON)
    ip_address = Column(String(50))
    user_agent = Column(String(500))
    created_at = Column(DateTime, default=datetime.now)
