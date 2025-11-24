import pytesseract
from PIL import Image
import os
import sys
import cv2
import numpy as np

class OCREngine:
    def __init__(self, config):
        self.config = config
        self._setup_tesseract_path()

    def _setup_tesseract_path(self):
        possible_paths = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
            os.path.join(os.getcwd(), "tesseract", "tesseract.exe"),
            os.path.join(os.path.dirname(sys.executable), "tesseract", "tesseract.exe"),
            os.path.join(os.getenv('LOCALAPPDATA', ''), 'Tesseract-OCR', 'tesseract.exe')
        ]
        
        found = False
        for path in possible_paths:
            if os.path.exists(path):
                pytesseract.pytesseract.tesseract_cmd = path
                
                # Check for local tessdata in app/assets/tessdata
                local_tessdata = os.path.join(os.getcwd(), "app", "assets", "tessdata")
                # Only use local folder if it actually has language files
                if os.path.exists(local_tessdata) and any(f.endswith('.traineddata') for f in os.listdir(local_tessdata)):
                     os.environ['TESSDATA_PREFIX'] = local_tessdata
                else:
                    # Fallback to system tessdata if not set
                    tessdata_dir = os.path.join(os.path.dirname(path), 'tessdata')
                    if os.path.exists(tessdata_dir) and 'TESSDATA_PREFIX' not in os.environ:
                        os.environ['TESSDATA_PREFIX'] = tessdata_dir
                
                found = True
                break

    def preprocess_image(self, pil_image):
        """
        Applies advanced preprocessing to remove background and enhance text.
        """
        # Convert PIL to OpenCV
        img = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply adaptive thresholding to handle uneven lighting/colored backgrounds
        # This is the key to fixing the "colored background" issue
        binary = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        
        # Denoise
        denoised = cv2.fastNlMeansDenoising(binary, None, 10, 7, 21)
        
        # Convert back to PIL
        return Image.fromarray(denoised)

    def create_searchable_pdf(self, image, output_path, lang='por'):
        """
        Creates a single page searchable PDF from an image.
        """
        try:
            pdf_bytes = pytesseract.image_to_pdf_or_hocr(image, extension='pdf', lang=lang)
            with open(output_path, 'wb') as f:
                f.write(pdf_bytes)
            return True
        except Exception as e:
            print(f"OCR PDF Generation Error: {e}")
            return False

    def get_available_languages(self):
        try:
            return pytesseract.get_languages()
        except:
            return []

    def is_available(self):
        try:
            pytesseract.get_tesseract_version()
            return True
        except:
            return False
