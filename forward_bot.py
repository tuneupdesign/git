# main.py - основной файл бота
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from flask import Flask
import threading

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_CHAT_ID = int(os.getenv("GROUP_CHAT_ID", "-1002512367222"))

async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

def main():
    # Создаем Flask app для Render
    app_flask = Flask(__name__)
    
    @app_flask.route('/')
    def home():
        return "Telegram Bot is running!"
    
    # Запускаем Flask в отдельном потоке
    threading.Thread(target=lambda: app_flask.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))).start()
    
    # Основной бот
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), forward_message))
    
    print("Бот запущен...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()