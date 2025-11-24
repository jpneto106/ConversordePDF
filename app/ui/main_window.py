from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                               QPushButton, QListWidget, QFileDialog, QProgressBar, 
                               QTextEdit, QLabel, QComboBox, QCheckBox, QGroupBox, QSplitter)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
import os

from app.ui.widgets import DragDropWidget
from app.ui.workers import ConversionWorker
from app.utils.i18n import I18n
from app.core.ocr import OCREngine

class MainWindow(QMainWindow):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.i18n = I18n(self.config.get("language", "pt_BR"))
        self.ocr_engine = OCREngine(self.config)
        
        self.files_to_convert = []
        self.worker = None
        
        self.init_ui()
        self.load_settings()

    def init_ui(self):
        self.setWindowTitle(self.i18n.get("app_title"))
        self.resize(1000, 700)
        
        # Main Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Header / Settings Row
        settings_layout = QHBoxLayout()
        
        # Language Selector
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["Português (BR)", "English (US)", "Español (ES)"])
        self.lang_combo.currentIndexChanged.connect(self.change_language)
        settings_layout.addWidget(QLabel(self.i18n.get("language") + ":"))
        settings_layout.addWidget(self.lang_combo)
        
        settings_layout.addStretch()
        
        # OCR Settings
        ocr_group = QGroupBox(self.i18n.get("ocr_settings"))
        ocr_layout = QHBoxLayout()
        self.ocr_check = QCheckBox(self.i18n.get("enable_ocr"))
        self.ocr_check.toggled.connect(self.on_ocr_toggled)
        ocr_layout.addWidget(self.ocr_check)
        
        self.ocr_lang_combo = QComboBox()
        # Populate with common Tesseract langs or defaults
        self.ocr_lang_combo.addItems(["por", "eng", "spa"]) 
        self.ocr_lang_combo.currentTextChanged.connect(self.save_settings)
        ocr_layout.addWidget(QLabel(self.i18n.get("ocr_lang") + ":"))
        ocr_layout.addWidget(self.ocr_lang_combo)
        
        ocr_group.setLayout(ocr_layout)
        settings_layout.addWidget(ocr_group)
        
        main_layout.addLayout(settings_layout)

        # Drag & Drop Area
        self.drag_drop = DragDropWidget(self.i18n)
        self.drag_drop.files_dropped.connect(self.add_files)
        self.drag_drop.setFixedHeight(100)
        main_layout.addWidget(self.drag_drop)

        # Content Splitter (File List vs Log)
        splitter = QSplitter(Qt.Vertical)
        
        # File List Area
        file_list_widget = QWidget()
        file_list_layout = QVBoxLayout(file_list_widget)
        file_list_layout.setContentsMargins(0,0,0,0)
        
        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton(self.i18n.get("select_files"))
        self.btn_add.clicked.connect(self.select_files)
        self.btn_clear = QPushButton(self.i18n.get("clear_all"))
        self.btn_clear.clicked.connect(self.clear_files)
        
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_clear)
        btn_layout.addStretch()
        
        self.file_list = QListWidget()
        
        file_list_layout.addLayout(btn_layout)
        file_list_layout.addWidget(self.file_list)
        splitter.addWidget(file_list_widget)

        # Log Area
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        splitter.addWidget(self.log_text)
        
        main_layout.addWidget(splitter)

        # Bottom Controls
        bottom_layout = QHBoxLayout()
        
        self.lbl_output = QLabel(self.i18n.get("select_folder"))
        self.btn_output = QPushButton("...")
        self.btn_output.clicked.connect(self.select_output_folder)
        
        bottom_layout.addWidget(QLabel(self.i18n.get("select_folder") + ":"))
        bottom_layout.addWidget(self.lbl_output)
        bottom_layout.addWidget(self.btn_output)
        
        bottom_layout.addStretch()
        
        self.btn_convert = QPushButton(self.i18n.get("convert"))
        self.btn_convert.setMinimumHeight(40)
        self.btn_convert.setMinimumWidth(150)
        self.btn_convert.setStyleSheet("background-color: #0078d7; color: white; font-weight: bold; border-radius: 5px;")
        self.btn_convert.clicked.connect(self.start_conversion)
        bottom_layout.addWidget(self.btn_convert)
        
        main_layout.addLayout(bottom_layout)

        # Progress Bar
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        main_layout.addWidget(self.progress)

        # Apply Styles
        self.apply_styles()

    def apply_styles(self):
        # Basic dark/light mode handling could go here
        pass

    def load_settings(self):
        lang_map = {"pt_BR": 0, "en_US": 1, "es_ES": 2}
        self.lang_combo.setCurrentIndex(lang_map.get(self.config.get("language"), 0))
        
        # Check if OCR is available before checking the box
        ocr_enabled = self.config.get("ocr_enabled", False)
        if ocr_enabled and not self.ocr_engine.is_available():
            ocr_enabled = False
            self.log("Warning: OCR disabled because Tesseract was not found.")
            
        self.ocr_check.setChecked(ocr_enabled)
        
        ocr_lang = self.config.get("ocr_language", "por")
        index = self.ocr_lang_combo.findText(ocr_lang)
        if index >= 0:
            self.ocr_lang_combo.setCurrentIndex(index)
            
        self.output_folder = self.config.get("output_folder", "")
        if self.output_folder:
            self.lbl_output.setText(self.output_folder)

    def on_ocr_toggled(self, checked):
        if checked:
            if not self.ocr_engine.is_available():
                from PySide6.QtWidgets import QMessageBox
                QMessageBox.warning(
                    self, 
                    "Tesseract OCR Missing", 
                    "Tesseract-OCR is not installed or not found.\n\n"
                    "Please install it from: https://github.com/UB-Mannheim/tesseract/wiki\n"
                    "And ensure it is in your PATH or standard installation folder."
                )
                self.ocr_check.setChecked(False)
                return
        self.save_settings()

    def save_settings(self):
        lang_codes = ["pt_BR", "en_US", "es_ES"]
        self.config.set("language", lang_codes[self.lang_combo.currentIndex()])
        self.config.set("ocr_enabled", self.ocr_check.isChecked())
        self.config.set("ocr_language", self.ocr_lang_combo.currentText())
        self.config.set("output_folder", self.output_folder)

    def change_language(self):
        self.save_settings()
        self.i18n.set_language(self.config.get("language"))
        self.retranslate_ui()

    def retranslate_ui(self):
        self.setWindowTitle(self.i18n.get("app_title"))
        self.drag_drop.update_text()
        self.btn_add.setText(self.i18n.get("select_files"))
        self.btn_clear.setText(self.i18n.get("clear_all"))
        self.btn_convert.setText(self.i18n.get("convert"))
        self.ocr_check.setText(self.i18n.get("enable_ocr"))
        # Update other labels...

    def select_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, self.i18n.get("select_files"), "", "PDF Files (*.pdf)")
        if files:
            self.add_files(files)

    def add_files(self, files):
        for f in files:
            if f not in self.files_to_convert:
                self.files_to_convert.append(f)
                self.file_list.addItem(os.path.basename(f))
        self.log(f"{len(files)} {self.i18n.get('files_selected')}")

    def clear_files(self):
        self.files_to_convert = []
        self.file_list.clear()

    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, self.i18n.get("select_folder"))
        if folder:
            self.output_folder = folder
            self.lbl_output.setText(folder)
            self.save_settings()

    def start_conversion(self):
        if not self.files_to_convert:
            self.log(self.i18n.get("error") + ": No files selected")
            return
        
        if not self.output_folder:
            self.log(self.i18n.get("error") + ": No output folder selected")
            return

        self.btn_convert.setEnabled(False)
        self.progress.setVisible(True)
        self.progress.setValue(0)
        
        self.worker = ConversionWorker(
            self.files_to_convert, 
            self.output_folder, 
            self.ocr_check.isChecked(), 
            self.ocr_lang_combo.currentText()
        )
        self.worker.progress_updated.connect(self.update_progress)
        self.worker.log_message.connect(self.log)
        self.worker.finished_all.connect(self.conversion_finished)
        self.worker.start()

    def update_progress(self, current, total, filename):
        percent = int((current / total) * 100)
        self.progress.setValue(percent)
        self.log(f"Processing: {filename}")

    def conversion_finished(self):
        self.btn_convert.setEnabled(True)
        self.progress.setVisible(False)
        self.log(self.i18n.get("completed"))

    def log(self, message):
        self.log_text.append(message)
