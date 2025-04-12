import csv
from typing import Dict
import logging
from importlib.resources import files

logger = logging.getLogger("kickstart-mcp")


class I18n:
    def __init__(self):
        self.current_lang = None
        self.resources: Dict[str, Dict[str, str]] = {}
        self.supported_languages = ["en", "ko", "zh", "ja"]
        self.default_lang = "en"

    def load_language(self, lang: str) -> None:
        """Load all CSV resource files for a specific language"""
        self.resources[lang] = {}
        try:
            locale_path = files("data.locales").joinpath(lang)
            for resource in locale_path.iterdir():
                if resource.name.endswith(".csv"):
                    try:
                        with resource.open("r", encoding="utf-8") as f:
                            reader = csv.DictReader(f)
                            for row in reader:
                                self.resources[lang][row["key"]] = row["value"]
                    except Exception as e:
                        logger.error(f"Error reading {resource.name}: {e}")
        except Exception as e:
            logger.error(f"Error loading language {lang}: {e}")

    def set_language(self, lang: str):
        """Set current language and load its resources"""
        if lang not in self.supported_languages:
            raise ValueError(f"Unsupported language: {lang}")

        if lang not in self.resources:
            self.load_language(lang)

        self.current_lang = lang
        logger.info(f"Language set to: {lang}")

    def get(self, key: str, *args) -> str:
        """Get a localized string for a key

        Args:
            key: The translation key to look up
            lang: Optional language code. If not provided, uses current_lang or default_lang
            *args: Variable positional arguments for string formatting

        Returns:
            The translated and formatted string, or the key if not found
        """
        if self.current_lang is not None:
            lang = self.current_lang
        else:
            lang = self.default_lang

        if lang not in self.resources:
            self.load_language(lang)

        if key in self.resources[lang]:
            text = self.resources[lang][key]
            try:
                # Only format if args are provided
                if args:
                    return text.format(*args)
                return text
            except Exception as e:
                logger.error(f"Error formatting text for key {key} with args {args}: {e}")
                return text
        elif lang != self.default_lang:
            # Fallback to default language
            if self.default_lang not in self.resources:
                self.load_language(self.default_lang)
            if key in self.resources[self.default_lang]:
                text = self.resources[self.default_lang][key]
                try:
                    if args:
                        return text.format(*args)
                    return text
                except Exception as e:
                    logger.error(f"Error formatting text for key {key} with args {args}: {e}")
                    return text

        return key  # Return the key itself if no translation found

    def get_available_languages(self) -> list[str]:
        """Get list of available languages by checking directories"""
        try:
            locale_path = files("kickstart_mcp.data.locales")
            return [d.name for d in locale_path.iterdir() if d.is_dir()]
        except Exception as e:
            logger.error(f"Error getting available languages: {e}")
            return [self.default_lang]


# Create a global instance
i18n = I18n()
