"""AI Service menggunakan Groq API."""
from groq import Groq
from config.settings import GROQ_API_KEY
from models import SessionLocal, KnowledgeBase
import logging

logger = logging.getLogger(__name__)

class AIService:
    """AI Assistant menggunakan Groq."""
    
    def __init__(self):
        try:
            self.client = Groq(api_key=GROQ_API_KEY)
            self.model = "llama-3.1-8b-instant"
            logger.info(f"AI Service initialized with {self.model}")
        except Exception as e:
            logger.error(f"Failed to initialize AI Service: {e}")
            self.client = None
    
    def get_context_from_kb(self, query: str) -> str:
        """Get relevant context from knowledge base."""
        db = SessionLocal()
        try:
            kb_entries = db.query(KnowledgeBase).all()
            
            relevant = []
            query_lower = query.lower()
            
            for entry in kb_entries:
                if entry.tags and any(keyword in query_lower for keyword in entry.tags.split(',')):
                    relevant.append(f"{entry.judul}:\n{entry.konten}")
            
            if relevant:
                return "\n\n".join(relevant[:2])
            return ""
        finally:
            db.close()
    
    def chat(self, user_message: str, employee_name: str = None) -> str:
        """Chat with AI assistant."""
        if not self.client:
            return "Maaf, AI Assistant sedang tidak tersedia."
        
        try:
            context = self.get_context_from_kb(user_message)
            
            system_prompt = """Kamu adalah asisten HR untuk BPKH (Badan Pengelola Keuangan Haji), lembaga pemerintah Indonesia yang mengelola dana haji.

Tugas kamu: membantu karyawan BPKH dengan pertanyaan tentang:
- Payroll dan gaji
- Cuti dan izin
- Absensi dan jam kerja
- Tunjangan dan benefit
- Kebijakan perusahaan

PENTING:
- Jawab dengan SINGKAT dan JELAS (maksimal 3-4 kalimat)
- Gunakan Bahasa Indonesia yang profesional
- Jika tidak tahu, arahkan ke menu yang relevan
- JANGAN membuat informasi yang tidak ada di knowledge base"""
            
            if context:
                system_prompt += f"\n\nInformasi dari knowledge base BPKH:\n{context}\n\nGunakan informasi ini untuk menjawab pertanyaan."
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.3,
                max_tokens=200  # Limit supaya jawaban lebih pendek
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"AI chat error: {e}")
            
            # Fallback to KB-only
            context = self.get_context_from_kb(user_message)
            if context:
                return f"Berikut informasi dari database BPKH:\n\n{context}"
            
            return "Maaf, saya tidak bisa menjawab pertanyaan itu. Silakan gunakan menu untuk akses fitur HR BPKH."

ai_service = AIService()
