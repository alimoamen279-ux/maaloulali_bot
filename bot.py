import os
import logging

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

if __name__ == "__main__":
    manager = AutoFolderNumberManager()
    print(f"Bot is running successfully with total {len(manager.allowed_numbers)} numbers from all .txt files!")

    
    
  

