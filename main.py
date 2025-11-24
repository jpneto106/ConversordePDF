import sys
import os
from PySide6.QtWidgets import QApplication
from app.ui.main_window import MainWindow
from app.core.config import ConfigManager

def main():
    # Ensure high DPI scaling
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    
    app = QApplication(sys.argv)
    app.setApplicationName("PDF to Word Converter")
    app.setOrganizationName("OpenSource")
    
    # Load configuration
    config = ConfigManager()
    
    # Initialize Main Window
    window = MainWindow(config)
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
