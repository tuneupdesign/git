from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

BOT_TOKEN = '8379582840:AAGACLYNbJqo4yws4Ii7L7pszkJwO9xVDrg'
GROUP_CHAT_ID = -1002512367222  # Вставь сюда chat_id своей группы

async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name or "пользователь"

    # Ответить отправителю
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

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), forward_message))

print("Бот запущен...")
app.run_polling()