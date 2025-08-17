"""
ভাষা এবং স্থানীয়করণ ইউটিলিটি
Language and Localization Utilities
"""

import json
import os
from typing import Dict, Any, Optional
from config.settings import config

class LocalizationManager:
    """স্থানীয়করণ ম্যানেজার - Localization Manager"""
    
    def __init__(self):
        self.messages: Dict[str, Dict[str, Any]] = {}
        self.load_all_languages()
    
    def load_all_languages(self):
        """Load all language files"""
        locales_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'locales')
        
        for lang_code in config.SUPPORTED_LANGUAGES:
            lang_file = os.path.join(locales_dir, lang_code, 'messages.json')
            if os.path.exists(lang_file):
                try:
                    with open(lang_file, 'r', encoding='utf-8') as f:
                        self.messages[lang_code] = json.load(f)
                    print(f"✅ Loaded {lang_code} language file")
                except Exception as e:
                    print(f"⚠️ Error loading {lang_code} language file: {e}")
            else:
                print(f"⚠️ Language file not found: {lang_file}")
    
    def get_text(self, key: str, lang_code: str = None, **kwargs) -> str:
        """Get localized text by key"""
        if lang_code is None:
            lang_code = config.DEFAULT_LANGUAGE
        
        if lang_code not in self.messages:
            lang_code = config.DEFAULT_LANGUAGE
        
        # Navigate through nested keys
        keys = key.split('.')
        text = self.messages[lang_code]
        
        try:
            for k in keys:
                text = text[k]
        except (KeyError, TypeError):
            return f"[Missing: {key}]"
        
        # Format with kwargs if provided
        if isinstance(text, str) and kwargs:
            try:
                text = text.format(**kwargs)
            except (KeyError, ValueError):
                pass
        
        return text
    
    def get_user_language(self, user) -> str:
        """Get user's preferred language"""
        if hasattr(user, 'language_code') and user.language_code in config.SUPPORTED_LANGUAGES:
            return user.language_code
        return config.DEFAULT_LANGUAGE

# Global instance
i18n = LocalizationManager()

def _(key: str, lang_code: str = None, **kwargs) -> str:
    """Shorthand function for getting localized text"""
    return i18n.get_text(key, lang_code, **kwargs)