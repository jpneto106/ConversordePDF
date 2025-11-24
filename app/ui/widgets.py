from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QFrame
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QDragEnterEvent, QDropEvent

class DragDropWidget(QFrame):
    files_dropped = Signal(list)

    def __init__(self, i18n):
        super().__init__()
        self.i18n = i18n
        self.setAcceptDrops(True)
        self.setObjectName("DragDropWidget")
        
        layout = QVBoxLayout()
        self.label = QLabel(self.i18n.get("drag_drop"))
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setObjectName("DragDropLabel")
        
        layout.addWidget(self.label)
        self.setLayout(layout)
        
        self.setStyleSheet("""
            QFrame#DragDropWidget {
                border: 2px dashed #aaa;
                border-radius: 10px;
                background-color: #f9f9f9;
            }
            QFrame#DragDropWidget:hover {
                border-color: #0078d7;
                background-color: #eef6ff;
            }
            QLabel#DragDropLabel {
                font-size: 16px;
                color: #555;
            }
        """)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        files = []
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if path.lower().endswith('.pdf'):
                files.append(path)
        
        if files:
            self.files_dropped.emit(files)

    def update_text(self):
        self.label.setText(self.i18n.get("drag_drop"))
