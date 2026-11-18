import os
import logging

# إعداد نظام التسجيل (Logging)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class MultiCountryNumberManager:
    # ضع هنا أسماء كل ملفات الدول المرفوعة في المستودع
    def __init__(self, filenames=["Egypt (1).txt", "Iraq_+964.txt"]):
        self.filenames = filenames
        self.allowed_numbers = set()
        self.load_all_numbers()

    def load_all_numbers(self):
        """
        قراءة جميع ملفات الأرقام المتاحة ودمجها في مجموعة واحدة (Set)
        """
        for filename in self.filenames:
            if not os.path.exists(filename):
                logging.error(f"الملف {filename} غير موجود.")
                continue

            try:
                with open(filename, 'r', encoding='utf-8') as file:
                    count = 0
                    for line in file:
                        cleaned_number = line.strip()
                        if cleaned_number:
                            self.allowed_numbers.add(cleaned_number)
                            count += 1
                logging.info(f"تم بنجاح تحميل {count} رقماً من ملف: {filename}")
            
            except Exception as e:
                logging.error(f"حدث خطأ أثناء قراءة الملف {filename}: {e}")

    def is_authorized(self, phone_number):
        if not phone_number:
            return False
        normalized_number = phone_number.strip()
        return normalized_number in self.allowed_numbers

if __name__ == "__main__":
    # تشغيل مدير الأرقام لجميع الدول معاً
    manager = MultiCountryNumberManager()
    print(f"Bot is running successfully with total {len(manager.allowed_numbers)} numbers from all files!")
    
    
    
  

