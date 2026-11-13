import os
from telegram.ext import ApplicationBuilder, CommandHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# استدعاء التوكن من متغيرات البيئة في ريل واي
BOT_TOKEN = os.getenv("BOT_TOKEN")

# دالة الترحيب وإرسال الرسالة مع الأزرار التفاعلية
async def start(update, context):
    # تصميم الأزرار (كل مصفوفة تمثل صفاً من الأزرار)
    keyboard = [
        [InlineKeyboardButton("📋 القائمة الرئيسية", callback_data="main_menu")],
        [InlineKeyboardButton("🌐 تغيير الدولة", callback_data="change_country")],
        [InlineKeyboardButton("🔑 جروب البوت", url="https://t.me/your_group")] # استبدل الرابط برابط جروبك الحقيقي
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # إرسال الرسالة مع الأزرار
    await update.message.reply_text(
        "أهلاً بك في بوت الخدمات والأرقام.\nاختر من الأزرار بالأسفل:",
        reply_markup=reply_markup
    )

def main():
    # إنشاء تطبيق البوت
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # ربط أمر /start بالدالة
    application.add_handler(CommandHandler("start", start))

    # تشغيل البوت بطريقة الـ Polling
    application.run_polling()

if __name__ == "__main__":
    main()
    
  

