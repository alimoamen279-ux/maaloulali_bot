import os
import logging

# إعداد نظام التسجيل (Logging) لتتبع الأخطاء والعمليات
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class IraqNumberManager:
    def __init__(self, filename="Iraq_+964.txt"):
        self.filename = filename
        self.allowed_numbers = set()
        self.load_numbers()

    def load_numbers(self):
        """
        قراءة ملف الأرقام وتحميلها إلى الذاكرة المؤقتة (Set)
        لتسريع عمليات البحث والتحقق اللاحقة.
        """
        if not os.path.exists(self.filename):
            logging.error(f"ملف الأرقام {self.filename} غير موجود في المسار الحالي.")
            return

        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                for line in file:
                    # تنظيف السطر من الفراغات والرموز الزائدة
                    cleaned_number = line.strip()
                    if cleaned_number:
                        self.allowed_numbers.add(cleaned_number)
            
            logging.info(f"تم بنجاح تحميل {len(self.allowed_numbers)} رقماً من الملف.")
        
        except Exception as e:
            logging.error(f"حدث خطأ غير متوقع أثناء قراءة الملف: {e}")

    def is_authorized(self, phone_number):
        """
        التحقق مما إذا كان الرقم المدخل موجوداً ضمن القائمة المعتمدة
        """
        if not phone_number:
            return False
        
        # تنظيف الرقم المدخل للتأكد من مطابقة التنسيق
        normalized_number = phone_number.strip()
        return normalized_number in self.allowed_numbers

# مثال متقدم لربط المدير ببوت (سواء كان Telegram أو Discord أو واجهة برمجية API)
if __name__ == "__main__":
    # تهيئة مدير الأرقام
    number_manager = IraqNumberManager()

    # اختبار رقم موجود في العينة مثل 9647885740254
    test_number_1 = "9647885740254"
    if number_manager.is_authorized(test_number_1):
        print(f"الرقم {test_number_1} معتمد في النظام وموجود ضمن القائمة.")
    else:
        print(f"الرقم {test_number_1} غير مسموح به.")

    # اختبار رقم غير موجود
    test_number_2 = "9640000000000"
    if number_manager.is_authorized(test_number_2):
        print(f"الرقم
        
  

