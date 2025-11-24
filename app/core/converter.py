from pdf2docx import Converter
import os
import fitz  # PyMuPDF
from PIL import Image
import io
import shutil
from app.core.ocr import OCREngine
from app.core.config import ConfigManager

class PDFConverter:
    def __init__(self, logger_callback=None):
        self.logger_callback = logger_callback
        self.config = ConfigManager()
        self.ocr_engine = OCREngine(self.config)

    def log(self, message):
        if self.logger_callback:
            self.logger_callback(message)
        else:
            print(message)

    def convert(self, input_path, output_folder, use_ocr=False, lang='por'):
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")

        filename = os.path.basename(input_path)
        name, _ = os.path.splitext(filename)
        output_path = os.path.join(output_folder, f"{name}.docx")
        
        # Temporary file for OCR processed PDF
        temp_pdf_path = os.path.join(output_folder, f"temp_{name}.pdf")

        self.log(f"Starting conversion: {filename}")

        try:
            source_file = input_path

            if use_ocr:
                self.log("OCR Enabled: Pre-processing pages (this may take a while)...")
                if not self.ocr_engine.is_available():
                    self.log("Warning: Tesseract not found. Skipping OCR.")
                else:
                    # OCR Pipeline
                    try:
                        processed_pdf = self._run_ocr_pipeline(input_path, temp_pdf_path, lang)
                        if processed_pdf:
                            source_file = temp_pdf_path
                            self.log("OCR Pre-processing complete. Converting to Word...")
                    except Exception as e:
                        self.log(f"OCR Pipeline failed: {e}. Falling back to standard conversion.")

            # Convert to Docx
            cv = Converter(source_file)
            cv.convert(output_path, start=0, end=None)
            cv.close()
            
            # Cleanup temp file
            if os.path.exists(temp_pdf_path):
                os.remove(temp_pdf_path)
            
            self.log(f"Finished: {output_path}")
            return True, output_path
            
        except Exception as e:
            self.log(f"Error converting {filename}: {str(e)}")
            # Cleanup on error
            if os.path.exists(temp_pdf_path):
                os.remove(temp_pdf_path)
            return False, str(e)

    def _run_ocr_pipeline(self, input_path, output_path, lang):
        """
        Renders PDF pages to images, preprocesses them, runs OCR, 
        and merges them back into a searchable PDF.
        """
        doc = fitz.open(input_path)
        pdf_merger = fitz.open() # Empty PDF to merge into
        
        temp_files = []
        
        total_pages = len(doc)
        for i, page in enumerate(doc):
            self.log(f"OCR Processing page {i+1}/{total_pages}...")
            
            # Render page to high-res image
            zoom = 2.0 # Higher zoom for better OCR
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            
            # Convert to PIL
            img_data = pix.tobytes("png")
            pil_image = Image.open(io.BytesIO(img_data))
            
            # Preprocess (Remove background, enhance contrast)
            processed_image = self.ocr_engine.preprocess_image(pil_image)
            
            # Save temp PDF page
            temp_page_pdf = f"{output_path}_page_{i}.pdf"
            success = self.ocr_engine.create_searchable_pdf(processed_image, temp_page_pdf, lang)
            
            if success:
                temp_files.append(temp_page_pdf)
                # Merge into main PDF
                with fitz.open(temp_page_pdf) as page_pdf:
                    pdf_merger.insert_pdf(page_pdf)
            else:
                self.log(f"Failed to OCR page {i+1}")

        # Save the final searchable PDF
        pdf_merger.save(output_path)
        pdf_merger.close()
        doc.close()
        
        # Cleanup temp page files
        for f in temp_files:
            if os.path.exists(f):
                os.remove(f)
                
        return True
