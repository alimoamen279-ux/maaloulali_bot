import os
from telegram.ext import ApplicationBuilder, CommandHandler

# استحباص التوكن من متغيرات البيئة في ريل واي
BOT_TOKEN = os.getenv("BOT_TOKEN")

# دالة الترحيب عند إرسال /start
async def start(update, context):
    await update.message.reply_text("أهلاً بك! البوت يعمل بنجاح تام.")

def main():
    # إنشاء تطبيق البوت
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # ربط أمر /start بالدالة
    application.add_handler(CommandHandler("start", start))

    # تشغيل البوت بطريقة الـ Polling
    application.run_polling()

if __name__ == "__main__":
    main()
  

