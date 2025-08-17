"""
বাংলা সহায়ক বট - প্রধান বট ক্লাস
Bengali Assistant Bot - Main Bot Class
"""

import logging
import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Any
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, CallbackQueryHandler,
    filters, ContextTypes, ConversationHandler
)

from config.settings import config
from config.database import db, User
from modules.utils.localization import i18n, _
from modules.utils.security import security
from modules.utils.bengali_calendar import bengali_calendar
from modules.tasks.task_manager import TaskManager
from modules.notifications.notification_manager import NotificationManager
from modules.user_management.profile_manager import ProfileManager
from modules.gamification.game_manager import GameManager
from modules.admin.admin_manager import AdminManager

# Conversation states
(WAITING_TASK_TITLE, WAITING_TASK_DESCRIPTION, WAITING_TASK_PRIORITY,
 WAITING_TASK_CATEGORY, WAITING_TASK_DUE_DATE, WAITING_VOICE_NOTE,
 WAITING_PROFILE_NAME, WAITING_BUG_REPORT) = range(8)

class BengaliBot:
    """বাংলা বট প্রধান ক্লাস - Main Bengali Bot Class"""
    
    def __init__(self):
        self.application: Optional[Application] = None
        self.task_manager = TaskManager()
        self.notification_manager = NotificationManager()
        self.profile_manager = ProfileManager()
        self.game_manager = GameManager()
        self.admin_manager = AdminManager()
        
        # Setup logging
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=getattr(logging, config.LOG_LEVEL.upper())
        )
        self.logger = logging.getLogger(__name__)
    
    async def initialize(self):
        """Initialize bot and database"""
        try:
            # Validate configuration
            config.validate()
            
            # Create database tables
            db.create_tables()
            
            # Build application
            self.application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()
            
            # Register handlers
            self._register_handlers()
            
            self.logger.info(f"🚀 {config.BOT_NAME} v{config.BOT_VERSION} initialized successfully!")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize bot: {e}")
            raise
    
    def _register_handlers(self):
        """Register all command and message handlers"""
        app = self.application
        
        # Command handlers
        app.add_handler(CommandHandler("start", self.start_command))
        app.add_handler(CommandHandler("help", self.help_command))
        app.add_handler(CommandHandler("profile", self.profile_command))
        app.add_handler(CommandHandler("tasks", self.tasks_command))
        app.add_handler(CommandHandler("calendar", self.calendar_command))
        app.add_handler(CommandHandler("settings", self.settings_command))
        app.add_handler(CommandHandler("quiz", self.quiz_command))
        app.add_handler(CommandHandler("leaderboard", self.leaderboard_command))
        app.add_handler(CommandHandler("admin", self.admin_command))
        app.add_handler(CommandHandler("bug", self.bug_report_command))
        
        # Conversation handler for task creation
        task_conv_handler = ConversationHandler(
            entry_points=[CallbackQueryHandler(self.create_task_start, pattern='^create_task$')],
            states={
                WAITING_TASK_TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.task_title_received)],
                WAITING_TASK_DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.task_description_received)],
                WAITING_TASK_PRIORITY: [CallbackQueryHandler(self.task_priority_selected, pattern='^priority_')],
                WAITING_TASK_CATEGORY: [CallbackQueryHandler(self.task_category_selected, pattern='^category_')],
                WAITING_TASK_DUE_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.task_due_date_received)],
                WAITING_VOICE_NOTE: [
                    MessageHandler(filters.VOICE, self.task_voice_received),
                    CommandHandler("skip", self.task_voice_skipped)
                ]
            },
            fallbacks=[CommandHandler("cancel", self.cancel_conversation)]
        )
        app.add_handler(task_conv_handler)
        
        # Callback query handlers
        app.add_handler(CallbackQueryHandler(self.handle_callback_query))
        
        # Voice and file handlers
        app.add_handler(MessageHandler(filters.VOICE, self.handle_voice))
        app.add_handler(MessageHandler(filters.Document.ALL, self.handle_document))
        app.add_handler(MessageHandler(filters.PHOTO, self.handle_photo))
        
        # General message handler
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        # Error handler
        app.add_error_handler(self.error_handler)
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user_data = update.effective_user
        user = db.get_or_create_user(
            telegram_id=user_data.id,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            username=user_data.username
        )
        
        lang = i18n.get_user_language(user)
        welcome_text = _(
            'welcome.greeting',
            lang_code=lang
        ) + "\n\n" + _(
            'welcome.description',
            lang_code=lang
        ) + "\n\n" + _(
            'welcome.getting_started',
            lang_code=lang
        )
        
        keyboard = self._get_main_menu_keyboard(lang)
        
        await update.message.reply_text(
            welcome_text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        
        # Log activity
        await self._log_activity(user.id, "start_command", "User started the bot")
    
    def _get_main_menu_keyboard(self, lang_code: str = 'bn') -> List[List[InlineKeyboardButton]]:
        """Get main menu keyboard"""
        return [
            [
                InlineKeyboardButton(_('menus.main_menu.tasks', lang_code=lang_code), callback_data='menu_tasks'),
                InlineKeyboardButton(_('menus.main_menu.calendar', lang_code=lang_code), callback_data='menu_calendar')
            ],
            [
                InlineKeyboardButton(_('menus.main_menu.profile', lang_code=lang_code), callback_data='menu_profile'),
                InlineKeyboardButton(_('menus.main_menu.notifications', lang_code=lang_code), callback_data='menu_notifications')
            ],
            [
                InlineKeyboardButton(_('menus.main_menu.games', lang_code=lang_code), callback_data='menu_games'),
                InlineKeyboardButton(_('menus.main_menu.help', lang_code=lang_code), callback_data='menu_help')
            ]
        ]
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        user = db.get_user_by_telegram_id(update.effective_user.id)
        lang = i18n.get_user_language(user)
        
        help_text = f"""
{_('help.title', lang_code=lang)}

{_('help.description', lang_code=lang)}

🚀 **{_('help.sections.getting_started', lang_code=lang)}:**
• /start - প্রধান মেনু
• /help - এই সাহায্য বার্তা

📝 **{_('help.sections.task_management', lang_code=lang)}:**
• /tasks - টাস্ক মেনু
• নতুন টাস্ক তৈরি করুন
• টাস্ক সম্পূর্ণ/সম্পাদনা করুন
• ভয়েস নোট দিয়ে টাস্ক তৈরি

🔔 **{_('help.sections.notifications', lang_code=lang)}:**
• দৈনিক/সাপ্তাহিক সারসংক্ষেপ
• টাস্ক রিমাইন্ডার
• অনুপ্রেরণামূলক বার্তা

📅 **{_('help.sections.calendar', lang_code=lang)}:**
• /calendar - বাংলা ক্যালেন্ডার
• আসন্ন ইভেন্ট
• ঋতু তথ্য

🎮 **{_('help.sections.games', lang_code=lang)}:**
• /quiz - দৈনিক কুইজ
• /leaderboard - লিডারবোর্ড
• পয়েন্ট ও অর্জন

⚙️ **{_('help.sections.settings', lang_code=lang)}:**
• /profile - প্রোফাইল সেটিংস
• /settings - বট সেটিংস
• ভাষা ও থিম পরিবর্তন

🔧 **{_('help.sections.troubleshooting', lang_code=lang)}:**
• /bug - বাগ রিপোর্ট করুন
• সাহায্যের জন্য @admin_username এ যোগাযোগ করুন
        """
        
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def calendar_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /calendar command"""
        user = db.get_user_by_telegram_id(update.effective_user.id)
        lang = i18n.get_user_language(user)
        
        # Get Bengali calendar info
        bengali_date_info = bengali_calendar.get_bengali_date()
        upcoming_events = bengali_calendar.get_upcoming_events()
        
        calendar_text = f"""
📅 **{_('calendar.today', lang_code=lang)}**

🗓️ **{_('calendar.bengali_date', lang_code=lang)}:** {bengali_date_info['bengali_date']}
📆 **{_('calendar.english_date', lang_code=lang)}:** {bengali_date_info['english_date']}
📅 **{_('calendar.day_name', lang_code=lang)}:** {bengali_date_info['bengali_weekday']}
🌸 **{_('calendar.season', lang_code=lang)}:** {bengali_date_info['season']}

⏰ **সময়:** {bengali_date_info['english_time']}

🎉 **আসন্ন অনুষ্ঠান:**
"""
        
        for event in upcoming_events:
            calendar_text += f"• {event['name']} - {event['bengali_date']}\n"
        
        # Get upcoming tasks
        upcoming_tasks = await self.task_manager.get_upcoming_tasks(user.id, days_ahead=3)
        if upcoming_tasks:
            calendar_text += f"\n📝 **{_('calendar.upcoming_tasks', lang_code=lang)}:**\n"
            for task in upcoming_tasks[:5]:
                calendar_text += f"• {task['title']} - {task['due_date']}\n"
        
        await update.message.reply_text(calendar_text, parse_mode='Markdown')
    
    async def handle_callback_query(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle inline keyboard callbacks"""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        user = db.get_user_by_telegram_id(query.from_user.id)
        lang = i18n.get_user_language(user)
        
        if data == 'menu_tasks':
            keyboard = [
                [
                    InlineKeyboardButton(_('menus.task_menu.create', lang_code=lang), callback_data='create_task'),
                    InlineKeyboardButton(_('menus.task_menu.view_all', lang_code=lang), callback_data='view_tasks')
                ],
                [
                    InlineKeyboardButton(_('menus.task_menu.pending', lang_code=lang), callback_data='pending_tasks'),
                    InlineKeyboardButton(_('menus.task_menu.completed', lang_code=lang), callback_data='completed_tasks')
                ],
                [
                    InlineKeyboardButton(_('buttons.back', lang_code=lang), callback_data='main_menu')
                ]
            ]
            await query.edit_message_text(
                f"📝 **{_('commands.tasks', lang_code=lang)}**\n\nআপনার টাস্ক ম্যানেজমেন্ট অপশন নির্বাচন করুন:",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode='Markdown'
            )
        
        elif data == 'main_menu':
            keyboard = self._get_main_menu_keyboard(lang)
            await query.edit_message_text(
                _('welcome.greeting', lang_code=lang),
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors"""
        self.logger.error(f"Exception while handling update: {context.error}")
        
        if update and update.effective_message:
            await update.effective_message.reply_text(
                _('errors.general', lang_code='bn'),
                parse_mode='Markdown'
            )
    
    async def _log_activity(self, user_id: int, action: str, description: str = None):
        """Log user activity"""
        try:
            # This would be implemented with the database
            pass
        except Exception as e:
            self.logger.error(f"Failed to log activity: {e}")
    
    def run(self):
        """Run the bot"""
        if not self.application:
            raise RuntimeError("Bot not initialized. Call initialize() first.")
        
        self.logger.info(f"🚀 Starting {config.BOT_NAME}...")
        self.application.run_polling()

# Placeholder methods for other handlers - these will be implemented in the respective modules
    async def profile_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE): pass
    async def tasks_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE): pass
    async def settings_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE): pass
    async def quiz_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE): pass
    async def leaderboard_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE): pass
    async def admin_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE): pass
    async def bug_report_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE): pass
    async def create_task_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE): pass
    async def task_title_received(self, update: Update, context: ContextTypes.DEFAULT_TYPE): pass
    async def task_description_received(self, update: Update, context: ContextTypes.DEFAULT_TYPE): pass
    async def task_priority_selected(self, update: Update, context: ContextTypes.DEFAULT_TYPE): pass
    async def task_category_selected(self, update: Update, context: ContextTypes.DEFAULT_TYPE): pass
    async def task_due_date_received(self, update: Update, context: ContextTypes.DEFAULT_TYPE): pass
    async def task_voice_received(self, update: Update, context: ContextTypes.DEFAULT_TYPE): pass
    async def task_voice_skipped(self, update: Update, context: ContextTypes.DEFAULT_TYPE): pass
    async def cancel_conversation(self, update: Update, context: ContextTypes.DEFAULT_TYPE): pass
    async def handle_voice(self, update: Update, context: ContextTypes.DEFAULT_TYPE): pass
    async def handle_document(self, update: Update, context: ContextTypes.DEFAULT_TYPE): pass
    async def handle_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE): pass
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE): pass