from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

async def print_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await update.message.reply_text(f"Chat ID этого чата: {chat_id}")
    print(f"Chat ID: {chat_id}")

app = ApplicationBuilder().token('8379582840:AAGACLYNbJqo4yws4Ii7L7pszkJwO9xVDrg').build()
app.add_handler(MessageHandler(filters.ALL, print_chat_id))
print("Жду сообщений...")
app.run_polling() -1002512367222