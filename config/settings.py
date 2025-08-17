"""
বাংলা টেলিগ্রাম বট - কনফিগারেশন সেটিংস
Bengali Telegram Bot - Configuration Settings
"""

import os
from typing import List, Optional

# Try to load dotenv if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️ python-dotenv not installed. Using environment variables only.")

class Config:
    # Telegram Bot Configuration
    TELEGRAM_BOT_TOKEN: str = os.getenv('TELEGRAM_BOT_TOKEN', '')
    WEBHOOK_URL: Optional[str] = os.getenv('WEBHOOK_URL')
    
    # Database Configuration
    DATABASE_URL: str = os.getenv('DATABASE_URL', 'sqlite:///bengali_bot.db')
    
    # Redis Configuration
    REDIS_URL: str = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    
    # Security
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'your-secret-key-here')
    ENCRYPTION_KEY: str = os.getenv('ENCRYPTION_KEY', '')
    
    # Admin Configuration
    ADMIN_USER_IDS: List[int] = [
        int(uid) for uid in os.getenv('ADMIN_USER_IDS', '').split(',') 
        if uid.strip().isdigit()
    ]
    SUPER_ADMIN_ID: Optional[int] = (
        int(os.getenv('SUPER_ADMIN_ID')) if os.getenv('SUPER_ADMIN_ID') else None
    )
    
    # File Configuration
    MAX_FILE_SIZE_MB: int = int(os.getenv('MAX_FILE_SIZE_MB', '50'))
    UPLOAD_FOLDER: str = os.getenv('UPLOAD_FOLDER', 'uploads/')
    
    # Notification Settings
    DAILY_SUMMARY_TIME: str = os.getenv('DAILY_SUMMARY_TIME', '09:00')
    WEEKLY_SUMMARY_DAY: int = int(os.getenv('WEEKLY_SUMMARY_DAY', '1'))
    MONTHLY_SUMMARY_DAY: int = int(os.getenv('MONTHLY_SUMMARY_DAY', '1'))
    
    # Development Settings
    DEBUG: bool = os.getenv('DEBUG', 'False').lower() in ('true', '1', 'yes')
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    
    # External APIs
    OPENWEATHER_API_KEY: str = os.getenv('OPENWEATHER_API_KEY', '')
    GOOGLE_TRANSLATE_API_KEY: str = os.getenv('GOOGLE_TRANSLATE_API_KEY', '')
    
    # Bengali Language Settings
    DEFAULT_LANGUAGE: str = 'bn'
    SUPPORTED_LANGUAGES: List[str] = ['bn', 'en']
    
    # Timezone
    TIMEZONE: str = 'Asia/Dhaka'
    
    # Bot Information
    BOT_NAME: str = 'বাংলা সহায়ক বট'
    BOT_VERSION: str = '1.0.0'
    BOT_DESCRIPTION: str = 'আধুনিক বাংলা টেলিগ্রাম বট - Modern Bengali Telegram Bot'
    
    @classmethod
    def validate(cls) -> bool:
        """Validate essential configuration"""
        if not cls.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN is required")
        
        if not cls.SECRET_KEY or cls.SECRET_KEY == 'your-secret-key-here':
            raise ValueError("SECRET_KEY must be set to a secure value")
            
        return True

# Create config instance
config = Config()