# Add this import at top of bot.py:
from utils.advanced_rag import advanced_rag

# Replace message_handler with this:
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('ai_mode'):
        user = update.effective_user
        db = SessionLocal()
        
        try:
            employee = db.query(Employee).filter(
                Employee.telegram_user_id == user.id
            ).first()
            
            if not employee:
                return
            
            user_message = update.message.text
            await update.message.chat.send_action("typing")
            
            # Use advanced RAG
            rag_result = advanced_rag.chat(
                query=user_message,
                employee_id=employee.id,
                user_id=user.id
            )
            
            response_text = f"í´– **Asisten AI:**\n\n{rag_result['response']}"
            
            # Add sources
            if rag_result['sources']:
                response_text += f"\n\ní³š Sumber: {', '.join(rag_result['sources'])}"
            
            response_text += "\n\nKetik /start untuk menu."
            
            await update.message.reply_text(response_text)
            
        finally:
            db.close()
