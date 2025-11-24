from PySide6.QtCore import QThread, Signal
from app.core.converter import PDFConverter

class ConversionWorker(QThread):
    progress_updated = Signal(int, int, str) # current, total, filename
    log_message = Signal(str)
    finished_all = Signal()
    
    def __init__(self, file_paths, output_folder, use_ocr, lang):
        super().__init__()
        self.file_paths = file_paths
        self.output_folder = output_folder
        self.use_ocr = use_ocr
        self.lang = lang
        self.is_running = True

    def run(self):
        converter = PDFConverter(logger_callback=self.emit_log)
        total = len(self.file_paths)
        
        for i, file_path in enumerate(self.file_paths):
            if not self.is_running:
                break
                
            self.progress_updated.emit(i + 1, total, file_path)
            self.emit_log(f"Processing {i+1}/{total}: {file_path}")
            
            success, msg = converter.convert(
                file_path, 
                self.output_folder, 
                self.use_ocr, 
                self.lang
            )
            
            if success:
                self.emit_log(f"Successfully converted: {file_path}")
            else:
                self.emit_log(f"Failed to convert {file_path}: {msg}")
                
        self.finished_all.emit()

    def emit_log(self, message):
        self.log_message.emit(message)

    def stop(self):
        self.is_running = False
