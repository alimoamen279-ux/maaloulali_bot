import os
import logging

# إعداد نظام التسجيل (Logging)
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
        """
        if not os.path.exists(self.filename):
            logging.error("File not found.")
            return

        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                for line in file:
                    cleaned_number = line.strip()
                    if cleaned_number:
                        self.allowed_numbers.add(cleaned_number)
            
            logging.info("Numbers loaded successfully.")
        
        except Exception as e:
            logging.error("An error occurred while reading the file.")

    def is_authorized(self, phone_number):
        if not phone_number:
            return False
        normalized_number = phone_number.strip()
        return normalized_number in self.allowed_numbers

if __name__ == "__main__":
    number_manager = IraqNumberManager()
    print("Bot is running successfully!")
    
  

