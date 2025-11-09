"""Knowledge Base model untuk RAG."""
from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from .database import Base

class KnowledgeBase(Base):
    __tablename__ = 'knowledge_base'
    
    id = Column(Integer, primary_key=True)
    kategori = Column(String(100))
    judul = Column(String(200))
    konten = Column(Text)
    tags = Column(String(500))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
