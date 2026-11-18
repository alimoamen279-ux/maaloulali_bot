import os
import logging
import telebot
from telebot import types

# توكن البوت (تأكد من وضعه هنا أو جلبه من متغيرات البيئة)
TOKEN = os.environ.get('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
bot = telebot.TeleBot(TOKEN)

# إعداد نظام التسجيل (Logging)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class AutoFolderNumberManager:
    def __init__(self):
        self.allowed_numbers = set()
        self.load_all_txt_files()

    def load_all_txt_files(self):
        """
        البحث تلقائياً عن جميع ملفات الـ .txt في المجلد وقراءتها دفعة واحدة
        """
        txt_files = [f for f in os.listdir('.') if f.endswith('.txt') and f != 'requirements.txt']
        
        if not txt_files:
            logging.error("لم يتم العثور على أي ملفات نصية (.txt) في المجلد الرئيسي!")
            return

        for filename in txt_files:
            try:
                with open(filename, 'r', encoding='utf-8') as file:
                    count = 0
                    for line in file:
                        cleaned_number = line.strip()
                        if cleaned_number:
                            self.allowed_numbers.add(cleaned_number)
                            count += 1
                logging.info(f"تم بنجاح تحميل {count} رقماً من الملف: {filename}")
            
            except Exception as e:
                logging.error(f"حدث خطأ أثناء قراءة الملف {filename}: {e}")

    def is_authorized(self, phone_number):
        if not phone_number:
            return False
        normalized_number = phone_number.strip()
        return normalized_number in self.allowed_numbers

# تشغيل مدير الأرقام وتحميلها في الذاكرة
number_manager = AutoFolderNumberManager()

# أمر البدء /start لإظهار الأزرار التفاعلية
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton("📞 الحصول على رقم", callback_data="get_number")
    btn2 = types.InlineKeyboardButton("🌍 تغيير الدولة", callback_data="change_country")
    btn3 = types.InlineKeyboardButton("🔑 جروب البوت", url="https://t.me/your_group_link") # ضع رابط جروبك هنا إذا أردت
    
    markup.add(btn1, btn2, btn3)
    
    bot.send_message(
        message.chat.id, 
        f"أهلاً بك في بوت الخدمات والأرقام! 🤖\nتم تحميل إجمالي {len(number_manager.allowed_numbers)} رقماً بنجاح.", 
        reply_markup=markup
    )

# معالج الأزرار التفاعلية (Callback Queries) لتجنب تعليق الأزرار
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "get_number":
        bot.answer_callback_query(call.id, "جاري إحضار الرقم...")
        bot.send_message(call.message.chat.id, "عفواً، يرجى إرسال رقم الهاتف للتحقق منه أولاً.")
    elif call.data == "change_country":
        bot.answer_callback_query(call.id, "اختر الدولة")
        bot.send_message(call.message.chat.id, "البوت يدعم حالياً جميع الدول المتاحة تلقائياً في الملفات المرفوعة.")

if __name__ == "__main__":
    print(f"Bot is running successfully with total {len(number_manager.allowed_numbers)} numbers from all .txt files!")
    # بدء تشغيل البوت باستمرار (Polling)
    bot.infinity_polling()


    
    
  

