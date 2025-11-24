import json
import os
import platform

class ConfigManager:
    def __init__(self):
        self.config_dir = self._get_config_dir()
        self.config_file = os.path.join(self.config_dir, "settings.json")
        self.default_config = {
            "language": "pt_BR",
            "output_folder": "",
            "theme": "dark",
            "ocr_enabled": False,
            "ocr_language": "por"
        }
        self.config = self.load_config()

    def _get_config_dir(self):
        """Returns the application data directory."""
        if platform.system() == "Windows":
            app_data = os.getenv("APPDATA")
            path = os.path.join(app_data, "PDFConverter")
        else:
            path = os.path.join(os.path.expanduser("~"), ".pdfconverter")
        
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    def load_config(self):
        """Loads configuration from JSON file."""
        if not os.path.exists(self.config_file):
            return self.default_config.copy()
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return self.default_config.copy()

    def save_config(self):
        """Saves current configuration to JSON file."""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4)
        except IOError as e:
            print(f"Error saving config: {e}")

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        self.save_config()
