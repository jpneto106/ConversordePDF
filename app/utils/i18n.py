class I18n:
    TRANSLATIONS = {
        "pt_BR": {
            "app_title": "Conversor PDF para Word",
            "select_files": "Selecionar Arquivos",
            "select_folder": "Selecionar Pasta de Saída",
            "convert": "Converter",
            "converting": "Convertendo...",
            "success": "Sucesso",
            "error": "Erro",
            "completed": "Conversão concluída!",
            "settings": "Configurações",
            "language": "Idioma",
            "ocr_settings": "Configurações de OCR",
            "enable_ocr": "Habilitar OCR (Lento)",
            "ocr_lang": "Idioma do OCR",
            "files_selected": "arquivos selecionados",
            "drag_drop": "Arraste e solte arquivos PDF aqui",
            "status_ready": "Pronto",
            "status_processing": "Processando {} de {}",
            "open_output": "Abrir Pasta",
            "remove": "Remover",
            "clear_all": "Limpar Tudo"
        },
        "en_US": {
            "app_title": "PDF to Word Converter",
            "select_files": "Select Files",
            "select_folder": "Select Output Folder",
            "convert": "Convert",
            "converting": "Converting...",
            "success": "Success",
            "error": "Error",
            "completed": "Conversion completed!",
            "settings": "Settings",
            "language": "Language",
            "ocr_settings": "OCR Settings",
            "enable_ocr": "Enable OCR (Slow)",
            "ocr_lang": "OCR Language",
            "files_selected": "files selected",
            "drag_drop": "Drag and drop PDF files here",
            "status_ready": "Ready",
            "status_processing": "Processing {} of {}",
            "open_output": "Open Folder",
            "remove": "Remove",
            "clear_all": "Clear All"
        },
        "es_ES": {
            "app_title": "Conversor PDF a Word",
            "select_files": "Seleccionar Archivos",
            "select_folder": "Seleccionar Carpeta de Salida",
            "convert": "Convertir",
            "converting": "Convirtiendo...",
            "success": "Éxito",
            "error": "Error",
            "completed": "¡Conversión completada!",
            "settings": "Configuraciones",
            "language": "Idioma",
            "ocr_settings": "Configuración de OCR",
            "enable_ocr": "Habilitar OCR (Lento)",
            "ocr_lang": "Idioma del OCR",
            "files_selected": "archivos seleccionados",
            "drag_drop": "Arrastre y suelte archivos PDF aquí",
            "status_ready": "Listo",
            "status_processing": "Procesando {} de {}",
            "open_output": "Abrir Carpeta",
            "remove": "Eliminar",
            "clear_all": "Limpiar Todo"
        }
    }

    def __init__(self, lang_code="pt_BR"):
        self.lang_code = lang_code if lang_code in self.TRANSLATIONS else "pt_BR"

    def set_language(self, lang_code):
        if lang_code in self.TRANSLATIONS:
            self.lang_code = lang_code

    def get(self, key):
        return self.TRANSLATIONS[self.lang_code].get(key, key)
