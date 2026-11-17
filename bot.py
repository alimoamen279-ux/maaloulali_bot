import os
import logging

# إعداد نظام التسجيل (Logging)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class EgyptNumberManager:
    def __init__(self, filename="Egypt (1).txt"):
        self.filename = filename
        self.allowed_numbers = set()
        self.load_numbers()

    def load_numbers(self):
        """
        قراءة ملف الأرقام المصري وتحميلها إلى الذاكرة المؤقتة (Set)
        """
        if not os.path.exists(self.filename):
            logging.error(f"الملف {self.filename} غير موجود.")
            return

        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                count = 0
                for line in file:
                    cleaned_number = line.strip()
                    if cleaned_number:
                        self.allowed_numbers.add(cleaned_number)
                        count += 1
            
            logging.info(f"تم بنجاح تحميل {count} رقماً مصرياً من الملف.")
        
        except Exception as e:
            logging.error(f"حدث خطأ أثناء قراءة الملف: {e}")

    def is_authorized(self, phone_number):
        if not phone_number:
            return False
        normalized_number = phone_number.strip()
        return normalized_number in self.allowed_numbers

if __name__ == "__main__":
    # تشغيل مدير الأرقام المصري فقط
    manager = EgyptNumberManager()
    print(f"Bot is running successfully with {len(manager.allowed_numbers)} Egyptian numbers!")
    
    
  

