# main.py - основной файл бота
import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from flask import Flask
import threading

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_CHAT_ID = int(os.getenv("GROUP_CHAT_ID", "-1002512367222"))

async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_name = update.effective_user.first_name or "пользователь"
        
        # Ответ отправителю
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Привет, {user_name}! Спасибо за сообщение. Мы скоро с тобой свяжемся 🤝"
        )
        
        # Переслать сообщение в группу
        await context.bot.forward_message(
            chat_id=GROUP_CHAT_ID,
            from_chat_id=update.effective_chat.id,
            message_id=update.message.message_id
        )
        
        logging.info(f"Message forwarded from {update.effective_user.id}")
        
    except Exception as e:
        logging.error(f"Error in forward_message: {e}")
        # Бот продолжит работать даже при ошибке

def main():
    # Создаем Flask app для Render (чтобы не требовал Background Worker)
    app_flask = Flask(__name__)
    
    @app_flask.route('/')
    def home():
        return "Telegram Bot is running!"
    
    @app_flask.route('/health')
    def health():
        return "OK", 200
    
    # Telegram бот
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), forward_message))
    
    print("Бот запущен...")
    
    # Запускаем Flask сервер в отдельном потоке
    def run_flask():
        app_flask.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)), debug=False, use_reloader=False)
    
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Запускаем бота с обработкой ошибок
    try:
        app.run_polling(
            drop_pending_updates=True,
            timeout=20,
            pool_timeout=20
        )
    except Exception as e:
        logging.error(f"Bot polling error: {e}")
        # Не завершаем процесс, пусть Render перезапустит

if __name__ == "__main__":
    main()