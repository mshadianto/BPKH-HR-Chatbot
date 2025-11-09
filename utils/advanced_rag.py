"""Advanced RAG with semantic search and agentic behavior."""
from models import SessionLocal, KnowledgeBase, Employee, Payroll
from groq import Groq
from config.settings import GROQ_API_KEY
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class AdvancedRAG:
    """Advanced RAG with agentic capabilities."""
    
    def __init__(self):
        try:
            self.client = Groq(api_key=GROQ_API_KEY)
            self.model = "llama-3.1-8b-instant"
            self.conversation_history = {}
            logger.info("Advanced RAG initialized")
        except Exception as e:
            logger.error(f"Failed to initialize RAG: {e}")
            self.client = None
    
    def expand_query(self, query: str) -> list:
        """Expand query dengan synonyms."""
        expansions = {
            'gaji': ['gaji', 'payroll', 'pembayaran', 'salary', 'penghasilan'],
            'cuti': ['cuti', 'leave', 'izin', 'off', 'libur'],
            'absen': ['absen', 'absensi', 'presensi', 'hadir', 'clock'],
            'tunjangan': ['tunjangan', 'benefit', 'allowance', 'insentif'],
        }
        
        query_lower = query.lower()
        expanded_terms = [query_lower]
        
        for key, synonyms in expansions.items():
            if key in query_lower:
                expanded_terms.extend(synonyms)
        
        return list(set(expanded_terms))
    
    def semantic_search_kb(self, query: str, top_k: int = 3) -> list:
        """Search KB with semantic matching."""
        db = SessionLocal()
        try:
            kb_entries = db.query(KnowledgeBase).all()
            expanded_terms = self.expand_query(query)
            
            scored_entries = []
            for entry in kb_entries:
                score = 0
                entry_text = f"{entry.judul} {entry.konten} {entry.tags}".lower()
                
                for term in expanded_terms:
                    score += entry_text.count(term)
                
                if any(term in entry.judul.lower() for term in expanded_terms):
                    score += 5
                
                if score > 0:
                    scored_entries.append({'entry': entry, 'score': score})
            
            scored_entries.sort(key=lambda x: x['score'], reverse=True)
            return [item['entry'] for item in scored_entries[:top_k]]
            
        finally:
            db.close()
    
    def get_employee_context(self, employee_id: int) -> str:
        """Get employee data for personalization."""
        db = SessionLocal()
        try:
            employee = db.query(Employee).filter(Employee.id == employee_id).first()
            if not employee:
                return ""
            
            current_month = datetime.now().strftime('%Y-%m')
            payroll = db.query(Payroll).filter(
                Payroll.employee_id == employee_id,
                Payroll.periode == current_month
            ).first()
            
            context = f"Employee: {employee.nama}, {employee.jabatan}, {employee.departemen}"
            
            if payroll:
                context += f", Gaji: Rp {payroll.total_gaji:,.0f}"
            
            return context
            
        finally:
            db.close()
    
    def detect_intent(self, query: str) -> dict:
        """Detect user intent."""
        query_lower = query.lower()
        
        intents = {
            'payroll': ['gaji', 'payroll', 'bayar', 'salary', 'penghasilan'],
            'cuti': ['cuti', 'leave', 'izin', 'libur'],
            'absensi': ['absen', 'clock', 'masuk', 'keluar', 'hadir'],
            'info': ['data', 'profil', 'informasi', 'nik'],
        }
        
        detected = []
        for intent, keywords in intents.items():
            if any(kw in query_lower for kw in keywords):
                detected.append(intent)
        
        return {
            'intents': detected,
            'has_intent': len(detected) > 0,
            'primary_intent': detected[0] if detected else None
        }
    
    def add_to_history(self, user_id: int, role: str, content: str):
        """Add to conversation history."""
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        self.conversation_history[user_id].append({
            'role': role,
            'content': content,
            'timestamp': datetime.now()
        })
        
        if len(self.conversation_history[user_id]) > 10:
            self.conversation_history[user_id] = self.conversation_history[user_id][-10:]
    
    def get_history(self, user_id: int, limit: int = 5) -> list:
        """Get conversation history."""
        if user_id not in self.conversation_history:
            return []
        return self.conversation_history[user_id][-limit:]
    
    def chat(self, query: str, employee_id: int = None, user_id: int = None) -> dict:
        """Advanced RAG chat."""
        if not self.client:
            return {
                'response': 'AI Assistant tidak tersedia.',
                'sources': [],
                'action': None
            }
        
        try:
            intent_data = self.detect_intent(query)
            kb_results = self.semantic_search_kb(query, top_k=2)
            
            emp_context = ""
            if employee_id:
                emp_context = self.get_employee_context(employee_id)
            
            history = []
            if user_id:
                history = self.get_history(user_id)
            
            kb_context = "\n\n".join([
                f"{entry.judul}: {entry.konten}" 
                for entry in kb_results
            ]) if kb_results else "Tidak ada info dari KB."
            
            system_prompt = f"""Asisten HR BPKH (Badan Pengelola Keuangan Haji).

Knowledge Base:
{kb_context}

{emp_context if emp_context else ''}

RULES:
- Jawab SINGKAT (max 3 kalimat)
- Bahasa Indonesia profesional
- Jika perlu aksi, suggest menu
- Jangan buat info palsu"""
            
            messages = [{"role": "system", "content": system_prompt}]
            
            for msg in history[-3:]:
                messages.append({"role": msg['role'], "content": msg['content']})
            
            messages.append({"role": "user", "content": query})
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.3,
                max_tokens=200
            )
            
            ai_response = response.choices[0].message.content
            
            suggested_action = None
            if intent_data['has_intent']:
                intent = intent_data['primary_intent']
                actions = {
                    'payroll': 'Untuk detail gaji, klik menu: Payroll',
                    'cuti': 'Untuk cuti, klik menu: Cuti',
                    'absensi': 'Untuk absensi, klik menu: Absensi',
                    'info': 'Untuk info lengkap, klik menu: Info'
                }
                suggested_action = actions.get(intent)
            
            if user_id:
                self.add_to_history(user_id, 'user', query)
                self.add_to_history(user_id, 'assistant', ai_response)
            
            final_response = ai_response
            if suggested_action:
                final_response += f"\n\n[TIP] {suggested_action}"
            
            return {
                'response': final_response,
                'sources': [entry.judul for entry in kb_results],
                'intent': intent_data['primary_intent'],
                'action': suggested_action
            }
            
        except Exception as e:
            logger.error(f"RAG error: {e}")
            
            kb_results = self.semantic_search_kb(query, top_k=1)
            if kb_results:
                entry = kb_results[0]
                return {
                    'response': f"{entry.judul}: {entry.konten}",
                    'sources': [entry.judul],
                    'action': None
                }
            
            return {
                'response': 'Maaf, tidak bisa menjawab. Gunakan menu.',
                'sources': [],
                'action': None
            }

advanced_rag = AdvancedRAG()
