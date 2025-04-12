import csv
from pathlib import Path
from typing import Dict, Optional
import logging

logger = logging.getLogger("kickstart-mcp")

class I18n:
    def __init__(self):
        self.current_lang = "en"
        self.resources: Dict[str, Dict[str, str]] = {}
        self.supported_languages = ["en", "ko"]

    def load_resources(self, lang: str):
        """Load all CSV resource files for a specific language"""
        self.resources[lang] = {}
        resource_path = Path(__file__).parent / "locales" / lang

        if not resource_path.exists():
            raise ValueError(f"Language resources not found: {lang}")

        for csv_file in resource_path.glob("*.csv"):
            try:
                with open(csv_file, "r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        key = row["key"]
                        self.resources[lang][key] = row["value"]
                logger.debug(f"Loaded resources from {csv_file}")
            except Exception as e:
                logger.error(f"Error loading resources from {csv_file}: {e}")
                raise

    def set_language(self, lang: str):
        """Set current language and load its resources"""
        if lang not in self.supported_languages:
            raise ValueError(f"Unsupported language: {lang}")

        if lang not in self.resources:
            self.load_resources(lang)

        self.current_lang = lang
        logger.info(f"Language set to: {lang}")

    def get_text(self, key: str) -> str:
        """Get localized text by key"""
        if self.current_lang not in self.resources:
            self.load_resources(self.current_lang)

        return self.resources[self.current_lang].get(key, key)

    def get_available_languages(self) -> list[str]:
        """Get list of available languages by checking directories"""
        locale_path = Path(__file__).parent / "locales"
        return [d.name for d in locale_path.iterdir() if d.is_dir() and d.name != "__pycache__"]

# Create a global instance
i18n = I18n()
