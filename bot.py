
import os
import logging
import random
import telebot
from telebot import types

TOKEN = os.environ.get('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
bot = telebot.TeleBot(TOKEN)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class AutoFolderNumberManager:
    def __init__(self):
        self.country_numbers = {} # تخزين الأرقام مقسمة حسب اسم الدولة
        self.load_all_txt_files()

    def load_all_txt_files(self):
        txt_files = [f for f in os.listdir('.') if f.endswith('.txt') and f != 'requirements.txt']
        
        if not txt_files:
            logging.error("لم يتم العثور على أي ملفات نصية (.txt) في المجلد الرئيسي!")
            return

        for filename in txt_files:
            country_name = filename.replace('.txt', '').strip()
            numbers_list = []
            try:
                with open(filename, 'r', encoding='utf-8') as file:
                    for line in file:
                        cleaned_number = line.strip()
                        if cleaned_number:
                            numbers_list.append(cleaned_number)
                
                if numbers_list:
                    self.country_numbers[country_name] = numbers_list
                    logging.info(f"تم بنجاح تحميل {len(numbers_list)} رقماً لدولة: {country_name}")
            
            except Exception as e:
                logging.error(f"حدث خطأ أثناء قراءة الملف {filename}: {e}")

number_manager = AutoFolderNumberManager()

# أمر البدء /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton("📞 الحصول على رقم", callback_data="get_number_menu")
    btn2 = types.InlineKeyboardButton("🌍 تغيير الدولة", callback_data="get_number_menu")
    btn3 = types.InlineKeyboardButton("🔑 جروب البوت", url="https://t.me/your_group_link")
    
    markup.add(btn1, btn2, btn3)
    
    bot.send_message(
        message.chat.id, 
        f"أهلاً بك في بوت الخدمات والأرقام! 🤖\nتم تحميل الأرقام من جميع الدول بنجاح.", 
        reply_markup=markup
    )

# عرض قائمة الدول عند الضغط على الحصول على رقم أو تغيير الدولة
@bot.callback_query_handler(func=lambda call: call.data in ["get_number_menu", "change_country"])
def show_countries(call):
    if not number_manager.country_numbers:
        bot.answer_callback_query(call.id, "عفواً، لا توجد دول متاحة حالياً.")
        return

    markup = types.InlineKeyboardMarkup(row_width=2)
    for country in number_manager.country_numbers.keys():
        # استخدام اسم الدولة كـ callback_data لجلب رقم منها لاحقاً
        markup.add(types.InlineKeyboardButton(f"🏳️ {country}", callback_data=f"select_{country}"))

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="اختر الدولة التي تريد الحصول على رقم منها:",
        reply_markup=markup
    )

# عند اختيار دولة معينة، يتم جلب رقم عشوائي منها وإرساله للمستخدم
@bot.callback_query_handler(func=lambda call: call.data.startswith("select_"))
def get_random_number_for_country(call):
    country_name = call.data.replace("select_", "")
    
    if country_name in number_manager.country_numbers:
        numbers_list = number_manager.country_numbers[country_name]
        if numbers_list:
            chosen_number = random.choice(numbers_list)
            bot.answer_callback_query(call.id, f"تم اختيار دولة {country_name} بنجاح!")
            
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("🔄 اختيار دولة أخرى", callback_data="change_country"))
            
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=f"📌 الدولة: **{country_name}**\n📞 الرقم هو:\n`{chosen_number}`",
                parse_mode="Markdown",
                reply_markup=markup
            )
        else:
            bot.answer_callback_query(call.id, "عفواً، هذه الدولة لا تحتوي على أرقام حالياً.")
    else:
        bot.answer_callback_query(call.id, "عفواً، حدث خطأ ما، يرجى المحاولة مرة أخرى.")

if __name__ == "__main__":
    bot.infinity_polling()


    
    
  

