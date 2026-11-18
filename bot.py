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
        self.country_numbers = {}
        self.load_all_txt_files()

    def load_all_txt_files(self):
        txt_files = [f for f in os.listdir('.') if f.endswith('.txt') and f != 'requirements.txt']
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
                    logging.info(f"تم تحميل {len(numbers_list)} رقماً لدولة: {country_name}")
            except Exception as e:
                logging.error(f"خطأ في قراءة {filename}: {e}")

number_manager = AutoFolderNumberManager()

def get_main_reply_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_get_num = types.KeyboardButton("📞 الحصول على رقم")
    btn_share = types.KeyboardButton("📊 شارك واربح")
    btn_stats = types.KeyboardButton("👤 الإحصائيات")
    btn_trafic = types.KeyboardButton("🔴 الترافيك المباشر")
    btn_prices = types.KeyboardButton("🌍 أرباح الدول")
    btn_about = types.KeyboardButton("ℹ️ حول البوت")
    markup.add(btn_get_num, btn_share, btn_stats, btn_trafic, btn_prices, btn_about)
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "🏠 **القائمة الرئيسية**\n\nاختر الخدمة المطلوبة من الأزرار بالأسفل:",
        parse_mode="Markdown",
        reply_markup=get_main_reply_keyboard()
    )

@bot.message_handler(func=lambda message: True)
def handle_text_messages(message):
    text = message.text
    chat_id = message.chat.id

    if text == "📞 الحصول على رقم":
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("📘 Facebook", callback_data="service_facebook"),
            types.InlineKeyboardButton("💚 WhatsApp", callback_data="service_whatsapp"),
            types.InlineKeyboardButton("📸 Instagram", callback_data="service_instagram"),
            types.InlineKeyboardButton("🎵 TikTok", callback_data="service_tiktok")
        )
        bot.send_message(chat_id, "🌐 **اختر الخدمة المطلوبة لتفعيل الأرقام** 👇", parse_mode="Markdown", reply_markup=markup)

    elif text == "👤 الإحصائيات":
        stats_text = (
            "📊 **إحصائياتك الخاصة**\n\n"
            f"👤 الاسم: {message.from_user.first_name}\n"
            f"🆔 معرفك: `{message.from_user.id}`\n"
            f"📦 إجمالي الأرقام المتاحة بالبوت: {sum(len(v) for v in number_manager.country_numbers.values())}"
        )
        bot.send_message(chat_id, stats_text, parse_mode="Markdown")

    elif text == "ℹ️ حول البوت":
        bot.send_message(chat_id, "🤖 هذا البوت مخصص لتوفير الأرقام والخدمات السريعة يعمل على مدار الساعة 24/7.")

    elif text in ["📊 شارك واربح", "🔴 الترافيك المباشر", "🌍 أرباح الدول"]:
        bot.send_message(chat_id, "🚧 هذه الميزة قيد التطوير وستتوفر قريباً!")

@bot.callback_query_handler(func=lambda call: call.data.startswith("service_"))
def show_countries_for_service(call):
    service_name = call.data.replace("service_", "").capitalize()
    if not number_manager.country_numbers:
        bot.answer_callback_query(call.id, "عفواً، لا توجد دول متاحة حالياً.")
        return

    markup = types.InlineKeyboardMarkup(row_width=2)
    country_buttons = []
    
    for country in number_manager.country_numbers.keys():
        country_buttons.append(types.InlineKeyboardButton(f"🏳️ {country}", callback_data=f"country_{country}"))
    
    markup.add(*country_buttons)
    markup.add(types.InlineKeyboardButton("🔙 الرجوع للخدمات", callback_data="back_to_services"))

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"📱 **اختر الدولة المناسبة لـ {service_name}** 👇",
        parse_mode="Markdown",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("country_") or call.data == "change_number_action")
def get_numbers_list(call):
    if call.data == "change_number_action":
        country_name = getattr(bot, 'last_country', list(number_manager.country_numbers.keys())[0])
    else:
        country_name = call.data.replace("country_", "")
        bot.last_country = country_name

    if country_name in number_manager.country_numbers:
        numbers_list = number_manager.country_numbers[country_name]
        sample_numbers = random.sample(numbers_list, min(4, len(numbers_list)))

        text_msg = (
            "⏳ **انتظار الكود...**\n"
            "🟢 **ستستلم الرسائل تلقائياً عند وصولها**\n"
        )

        markup = types.InlineKeyboardMarkup(row_width=1)
        for num in sample_numbers:
            markup.add(types.InlineKeyboardButton(f"📋 +{num}", callback_data=f"copy_{num}"))

        markup.add(
            types.InlineKeyboardButton("🔄 تغيير الرقم", callback_data="change_number_action"),
            types.InlineKeyboardButton("🌍 تغيير الدولة", callback_data="back_to_services"),
            types.InlineKeyboardButton("🔑 جروب البوت", url="https://t.me/your_group_link"),
            types.InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")
        )

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text_msg,
            parse_mode="Markdown",
            reply_markup=markup
        )

@bot.callback_query_handler(func=lambda call: call.data.startswith("copy_"))
def handle_copy_number(call):
    phone_num = call.data.replace("copy_", "")
    bot.answer_callback_query(call.id, f"تم نسخ الرقم: +{phone_num}", show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data in ["back_to_services", "main_menu"])
def back_navigation(call):
    if call.data == "back_to_services":
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("📘 Facebook", callback_data="service_facebook"),
            types.InlineKeyboardButton("💚 WhatsApp", callback_data="service_whatsapp"),
            types.InlineKeyboardButton("📸 Instagram", callback_data="service_instagram"),
            types.InlineKeyboardButton("🎵 TikTok", callback_data="service_tiktok")
        )
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🌐 **اختر الخدمة المطلوبة لتفعيل الأرقام** 👇", parse_mode="Markdown", reply_markup=markup)
    elif call.data == "main_menu":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "🏠 **القائمة الرئيسية**", reply_markup=get_main_reply_keyboard())

if __name__ == "__main__":
    bot.infinity_polling()

                    




    
    
  

