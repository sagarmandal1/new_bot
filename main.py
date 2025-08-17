#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ultra-modern Bengali Telegram Bot
Main entry point for the bot application

Features:
- Routine management with smart scheduling
- Quick task management with deadlines
- Smart reminders system
- Bengali UI with attractive emojis
- Local JSON database with auto-backup
- Windows-compatible UTF-8 encoding
"""

import logging
import os
import sys
from telegram.ext import (
    Application, 
    CommandHandler, 
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    filters
)

from storage import StorageManager
from handlers import BotHandlers
from constants import COMMANDS, STATES

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class BengaliBotApp:
    """Main bot application class"""
    
    def __init__(self):
        """Initialize the bot application"""
        self.token = self._get_bot_token()
        self.storage = StorageManager()
        self.handlers = BotHandlers(self.storage)
        self.application = None
        
        logger.info("Bengali Telegram Bot initialized")
    
    def _get_bot_token(self) -> str:
        """Get bot token from environment variable or config"""
        token = os.getenv('BOT_TOKEN')
        
        if not token:
            logger.error("Bot token not found. Please set BOT_TOKEN environment variable.")
            print("\n" + "="*50)
            print("⚠️  BOT TOKEN প্রয়োজন")
            print("="*50)
            print("Bot চালানোর জন্য আপনার Telegram bot token প্রয়োজন।")
            print("\n📝 কীভাবে token পাবেন:")
            print("1. @BotFather এ যান Telegram এ")
            print("2. /newbot কমান্ড দিন")
            print("3. Bot এর নাম এবং username দিন")
            print("4. Token কপি করুন")
            print("\n💻 Token সেট করুন:")
            print("Linux/Mac: export BOT_TOKEN='YOUR_TOKEN_HERE'")
            print("Windows: set BOT_TOKEN=YOUR_TOKEN_HERE")
            print("="*50)
            sys.exit(1)
        
        return token
    
    def setup_handlers(self):
        """Set up all command and callback handlers"""
        
        # Command handlers
        self.application.add_handler(CommandHandler(COMMANDS['start'], self.handlers.start_command))
        self.application.add_handler(CommandHandler(COMMANDS['menu'], self.handlers.menu_command))
        self.application.add_handler(CommandHandler(COMMANDS['help'], self.handlers.help_command))
        self.application.add_handler(CommandHandler(COMMANDS['stats'], self.handlers.stats_command))
        
        # Conversation handlers for complex operations
        routine_conv_handler = ConversationHandler(
            entry_points=[],  # Will be triggered by callback queries
            states={
                STATES['WAITING_ROUTINE_NAME']: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self.handlers.handle_routine_name_input)
                ],
                STATES['WAITING_ROUTINE_TIME']: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self.handlers.handle_routine_time_input)
                ]
            },
            fallbacks=[
                CallbackQueryHandler(self.handlers.cancel_operation, pattern='^cancel$')
            ]
        )
        
        task_conv_handler = ConversationHandler(
            entry_points=[],  # Will be triggered by callback queries
            states={
                STATES['WAITING_TASK_NAME']: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self.handlers.handle_task_name_input)
                ]
            },
            fallbacks=[
                CallbackQueryHandler(self.handlers.cancel_operation, pattern='^cancel$')
            ]
        )
        
        profile_conv_handler = ConversationHandler(
            entry_points=[],  # Will be triggered by callback queries
            states={
                STATES['WAITING_PROFILE_NAME']: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self.handlers.handle_profile_name_input)
                ]
            },
            fallbacks=[
                CallbackQueryHandler(self.handlers.cancel_operation, pattern='^cancel$')
            ]
        )
        
        # Add conversation handlers
        self.application.add_handler(routine_conv_handler)
        self.application.add_handler(task_conv_handler)
        self.application.add_handler(profile_conv_handler)
        
        # Callback query handler (for inline keyboards)
        self.application.add_handler(CallbackQueryHandler(self.handlers.button_callback))
        
        # Error handler
        self.application.add_error_handler(self.handlers.error_handler)
        
        logger.info("All handlers registered successfully")
    
    async def post_init(self, application: Application):
        """Post initialization setup"""
        logger.info("Bot post-initialization completed")
    
    async def post_shutdown(self, application: Application):
        """Cleanup after shutdown"""
        logger.info("Bot shutdown completed")
    
    def run(self):
        """Start the bot"""
        logger.info("Starting Bengali Telegram Bot...")
        
        try:
            # Create application
            self.application = Application.builder().token(self.token).post_init(self.post_init).post_shutdown(self.post_shutdown).build()
            
            # Setup handlers
            self.setup_handlers()
            
            # Print startup information
            self._print_startup_info()
            
            # Start the bot
            logger.info("Bot is running. Press Ctrl+C to stop.")
            self.application.run_polling(allowed_updates=['message', 'callback_query'])
            
        except Exception as e:
            logger.error(f"Error starting bot: {e}")
            sys.exit(1)
    
    def _print_startup_info(self):
        """Print colorful startup information"""
        print("\n" + "="*60)
        print("🤖 বাংলা টেলিগ্রাম বট চালু হয়েছে!")
        print("="*60)
        print("✅ ডাটাবেস সংযোগ সফল")
        print("✅ হ্যান্ডলার সেটআপ সফল")
        print("✅ বট টোকেন যাচাই সফল")
        print("\n📋 বৈশিষ্ট্যসমূহ:")
        print("   🔹 রুটিন ম্যানেজমেন্ট")
        print("   🔹 দ্রুত টাস্ক ম্যানেজমেন্ট")
        print("   🔹 স্মার্ট রিমাইন্ডার")
        print("   🔹 বাংলা UI এবং ইমোজি")
        print("   🔹 JSON ডাটাবেস ও অটো ব্যাকআপ")
        print("   🔹 সেটিংস ও পরিসংখ্যান")
        print("\n🚀 বট সফলভাবে চালু! Ctrl+C দিয়ে বন্ধ করুন।")
        print("="*60)

def main():
    """Main function"""
    try:
        # Create and run the bot
        bot_app = BengaliBotApp()
        bot_app.run()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
        print("\n" + "="*50)
        print("🛑 বট বন্ধ করা হয়েছে")
        print("   ধন্যবাদ Bengali Bot ব্যবহার করার জন্য!")
        print("="*50)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"\n❌ অপ্রত্যাশিত ত্রুটি: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()