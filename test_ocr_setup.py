from app.core.ocr import OCREngine
from app.core.config import ConfigManager
import sys

try:
    config = ConfigManager()
    ocr = OCREngine(config)
    print(f"OCR Available: {ocr.is_available()}")
    
    # Manually set path if not found (just to be sure for the test)
    import pytesseract
    if not ocr.is_available():
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        print(f"OCR Available after manual set: {ocr.is_available()}")

    langs = ocr.get_available_languages()
    print(f"Available Languages: {langs}")
    
except Exception as e:
    print(f"Error: {e}")
