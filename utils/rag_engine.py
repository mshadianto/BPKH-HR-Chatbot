"""RAG Engine menggunakan Groq API (pengganti OpenAI)."""
import os
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from config.settings import GROQ_API_KEY, CHROMA_DB_PATH, EMBEDDING_MODEL, LLM_MODEL

class RAGEngine:
    """RAG Engine untuk menjawab pertanyaan berdasarkan knowledge base."""
    
    def __init__(self):
        """Initialize RAG engine with Groq."""
        # Use local embeddings (free & fast)
        self.embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        # Initialize vector store
        self.vectorstore = Chroma(
            persist_directory=CHROMA_DB_PATH,
            embedding_function=self.embeddings
        )
        
        # Initialize Groq LLM
        self.llm = ChatGroq(
            groq_api_key=GROQ_API_KEY,
            model_name=LLM_MODEL,
            temperature=0.3,
            max_tokens=1024
        )
        
        # Custom prompt template untuk HR Bot
        template = """Kamu adalah asisten HR BPKH (Badan Pengelola Keuangan Haji) yang membantu karyawan dengan pertanyaan seputar kebijakan perusahaan, prosedur, dan informasi HR. 

Berdasarkan konteks berikut, jawab pertanyaan dengan ramah, informatif, dan profesional.

Konteks: {context}

Pertanyaan: {question}

Jawaban (dalam Bahasa Indonesia yang sopan dan mudah dipahami):"""
        
        PROMPT = PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
        
        # Create QA chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 3}),
            chain_type_kwargs={"prompt": PROMPT}
        )
    
    def query(self, question: str) -> str:
        """Query the RAG engine."""
        try:
            result = self.qa_chain.run(question)
            return result
        except Exception as e:
            return f"Maaf, terjadi kesalahan: {str(e)}\n\nPastikan Groq API key sudah benar di .env file."
    
    def add_documents(self, documents):
        """Add documents to vector store."""
        self.vectorstore.add_documents(documents)
        self.vectorstore.persist()
