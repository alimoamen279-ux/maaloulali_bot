import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

TOKEN = os.getenv("BOT_TOKEN")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.reply_text(f"أهلاً بك! لقد استلمت رسالتك: {user_message}")

def main():
    if not TOKEN:
        print("Error: BOT_TOKEN is not set!")
        return

    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))
    
    print("Bot is running...")
    application.run_polling()

if __name__ == '__main__':
    main()
  
