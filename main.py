#!/usr/bin/env python3
"""
Daily Routine Update Bot
দৈনিক রুটিন আপডেট বট

A comprehensive Telegram bot for managing daily routines with Bengali language support.
"""

import logging
import json
import asyncio
from datetime import datetime, timedelta

from telegram import Update
from telegram.ext import (
    Application, 
    CommandHandler, 
    MessageHandler, 
    CallbackQueryHandler,
    ConversationHandler,
    filters
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

# Import our services and handlers
from bot.utils.database import JSONDatabase
from bot.services.user_service import UserService
from bot.services.routine_service import RoutineService
from bot.services.notification_service import NotificationService
from bot.services.backup_service import BackupService

from bot.handlers.user_handlers import UserHandlers, get_registration_conversation_handler
from bot.handlers.routine_handlers import RoutineHandlers, get_create_routine_conversation_handler
from bot.handlers.report_handlers import ReportHandlers
from bot.handlers.admin_handlers import AdminHandlers, get_broadcast_conversation_handler

from bot.utils.helpers import get_text

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class DailyRoutineBot:
    """Main bot class"""
    
    def __init__(self, config_file: str = "config.json"):
        # Load configuration
        with open(config_file, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        # Initialize database
        self.db = JSONDatabase()
        
        # Initialize services
        self.user_service = UserService(self.db)
        self.routine_service = RoutineService(self.db)
        self.backup_service = BackupService(self.db)
        
        # Initialize application
        self.application = Application.builder().token(self.config['bot_token']).build()
        
        # Initialize notification service (needs bot instance)
        self.notification_service = NotificationService(
            self.application.bot, 
            self.routine_service, 
            self.user_service
        )
        
        # Initialize handlers
        self.user_handlers = UserHandlers(self.user_service)
        self.routine_handlers = RoutineHandlers(self.routine_service, self.user_service)
        self.report_handlers = ReportHandlers(self.routine_service, self.user_service)
        self.admin_handlers = AdminHandlers(
            self.user_service, 
            self.notification_service, 
            self.backup_service,
            self.config['admin_user_ids']
        )
        
        # Initialize scheduler
        self.scheduler = AsyncIOScheduler()
        
        # Setup handlers
        self._setup_handlers()
        self._setup_scheduler()
    
    def _setup_handlers(self):
        """Setup all bot handlers"""
        app = self.application
        
        # Command handlers
        app.add_handler(CommandHandler("start", self.user_handlers.start_command))
        app.add_handler(CommandHandler("help", self.user_handlers.help_command))
        app.add_handler(CommandHandler("menu", self.user_handlers.menu_command))
        app.add_handler(CommandHandler("profile", self.user_handlers.profile_command))
        app.add_handler(CommandHandler("settings", self.user_handlers.settings_command))
        
        # Registration conversation
        app.add_handler(get_registration_conversation_handler(self.user_handlers))
        
        # Routine commands
        app.add_handler(CommandHandler("my_routines", self.routine_handlers.my_routines_command))
        app.add_handler(CommandHandler("today", self.routine_handlers.today_routine_command))
        
        # Create routine conversation
        app.add_handler(get_create_routine_conversation_handler(self.routine_handlers))
        
        # Report commands
        app.add_handler(CommandHandler("daily_report", self.report_handlers.reports_menu))
        app.add_handler(CommandHandler("weekly_report", self.report_handlers.reports_menu))
        app.add_handler(CommandHandler("monthly_report", self.report_handlers.reports_menu))
        
        # Admin commands
        app.add_handler(CommandHandler("admin", self.admin_handlers.admin_command))
        
        # Broadcast conversation (for admin)
        app.add_handler(get_broadcast_conversation_handler(self.admin_handlers))
        
        # Callback query handlers
        app.add_handler(CallbackQueryHandler(
            self.user_handlers.settings_callback, 
            pattern=r'^(settings_|lang_)'
        ))
        app.add_handler(CallbackQueryHandler(
            self.routine_handlers.routine_callback, 
            pattern=r'^(routine_|complete_|delete_|toggle_|skip_|postpone_)'
        ))
        app.add_handler(CallbackQueryHandler(
            self.routine_handlers.create_routine_frequency,
            pattern=r'^freq_'
        ))
        app.add_handler(CallbackQueryHandler(
            self.report_handlers.report_callback,
            pattern=r'^report_'
        ))
        app.add_handler(CallbackQueryHandler(
            self.admin_handlers.admin_callback,
            pattern=r'^admin_'
        ))
        
        # Message handlers for menu buttons
        app.add_handler(MessageHandler(
            filters.Text("📝 রুটিন তৈরি"), 
            self.routine_handlers.create_routine_command
        ))
        app.add_handler(MessageHandler(
            filters.Text("📋 আমার রুটিনসমূহ"), 
            self.routine_handlers.my_routines_command
        ))
        app.add_handler(MessageHandler(
            filters.Text("📅 আজকের রুটিন"), 
            self.routine_handlers.today_routine_command
        ))
        app.add_handler(MessageHandler(
            filters.Text("📊 রিপোর্ট"), 
            self.report_handlers.reports_menu
        ))
        app.add_handler(MessageHandler(
            filters.Text("⚙️ সেটিংস"), 
            self.user_handlers.settings_command
        ))
        app.add_handler(MessageHandler(
            filters.Text("❓ সাহায্য"), 
            self.user_handlers.help_command
        ))
        
        # Support command
        app.add_handler(CommandHandler("support", self.support_command))
        
        # Error handler
        app.add_error_handler(self.error_handler)
    
    def _setup_scheduler(self):
        """Setup scheduled tasks"""
        # Send routine reminders every minute
        self.scheduler.add_job(
            self.notification_service.send_routine_reminders,
            CronTrigger(second=0),  # Every minute at 0 seconds
            id='routine_reminders'
        )
        
        # Create automatic backups daily at 2 AM
        self.scheduler.add_job(
            self.backup_service.create_backup,
            CronTrigger(hour=2, minute=0),
            id='daily_backup'
        )
        
        # Send daily summaries at 9 PM
        self.scheduler.add_job(
            self.send_daily_summaries,
            CronTrigger(hour=21, minute=0),
            id='daily_summaries'
        )
    
    async def send_daily_summaries(self):
        """Send daily summaries to all users"""
        users = self.user_service.get_all_users()
        
        for user_id_str in users.keys():
            user_id = int(user_id_str)
            user_data = users[user_id_str]
            
            # Check if user wants notifications
            if user_data.get('notifications_enabled', True):
                try:
                    await self.notification_service.send_daily_summary(user_id)
                except Exception as e:
                    logger.error(f"Failed to send daily summary to {user_id}: {e}")
    
    async def support_command(self, update: Update, context):
        """Handle support command"""
        user_id = update.effective_user.id
        user_lang = self.user_service.get_user_language(user_id)
        text = get_text(user_lang)
        
        support_text = """
🛠️ *সাহায্য ও সহায়তা*

যদি আপনার কোন সমস্যা হয় বা প্রশ্ন থাকে:

📧 ইমেইল: support@dailyroutinebot.com
💬 টেলিগ্রাম: @DailyRoutineSupport

*সাধারণ সমস্যা সমাধান:*

1. **রুটিন তৈরি করতে পারছি না**
   → /register দিয়ে প্রথমে নিবন্ধন করুন

2. **নোটিফিকেশন আসছে না**
   → /settings থেকে নোটিফিকেশন চালু করুন

3. **বট সাড়া দিচ্ছে না**
   → /start দিয়ে আবার শুরু করুন

4. **ডেটা হারিয়ে গেছে**
   → অ্যাডমিনের সাথে যোগাযোগ করুন

🤖 *বট সংস্করণ:* v1.0.0
        """
        
        await update.message.reply_text(support_text, parse_mode='Markdown')
    
    async def error_handler(self, update: Update, context):
        """Handle errors"""
        logger.error(f"Exception while handling an update: {context.error}")
        
        # Try to send error message to user
        if update and update.effective_user:
            try:
                user_id = update.effective_user.id
                user_lang = self.user_service.get_user_language(user_id)
                text = get_text(user_lang)
                
                await update.message.reply_text(
                    text.get("error_occurred", "❌ একটি ত্রুটি ঘটেছে। আবার চেষ্টা করুন।")
                )
            except Exception as e:
                logger.error(f"Failed to send error message: {e}")
    
    def run(self):
        """Run the bot"""
        logger.info("🤖 দৈনিক রুটিন বট শুরু হচ্ছে...")
        logger.info("🗄️ ডেটাবেস ইনিশিয়ালাইজ হয়েছে")
        logger.info("⏰ শিডিউলার শুরু হচ্ছে...")
        
        # Start scheduler
        self.scheduler.start()
        
        logger.info("🚀 বট চালু হয়েছে!")
        
        # Run bot
        self.application.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True
        )

def main():
    """Main function"""
    try:
        bot = DailyRoutineBot()
        bot.run()
    except KeyboardInterrupt:
        logger.info("🛑 বট বন্ধ করা হচ্ছে...")
    except Exception as e:
        logger.error(f"❌ বট চালানোয় ত্রুটি: {e}")

if __name__ == "__main__":
    main()